import json
import os
from contextlib import asynccontextmanager
from typing import Dict, Any, Union, List

import fastapi
import pydantic
from fastapi import FastAPI
import requests
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import schema_of

from hueplex import payload
from hueplex.models.base import BaseEvent

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {
        'hue_key': os.getenv('HUE_KEY', None)
    }



app = FastAPI(lifespan=lifespan)

request_data = {}


class PrettyJSONResponse(fastapi.responses.JSONResponse):

    def render(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
            separators=(",", ":"),
        ).encode("utf-8")


@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def handle_validation_error(request: fastapi.Request, exc: fastapi.exceptions.RequestValidationError | pydantic.ValidationError):

    errors = request_data.get('errors', [])
    errors.append(
        {
            'body': exc.body,
            'detail': exc.errors(),
        },
    )
    request_data['errors'] = errors

    return request_validation_exception_handler(request, exc)



def handle_media_command(command: str, hue_key: str):

    light = 'ae8cef70-3421-4fb7-a5db-07aae0ef319b'

    match command:
        case "play" | "resume":
            on = False
        case "pause" | "stop":
            on = True
        case _:
            return

    requests.put(
        f'https://192.168.1.11/clip/v2/resource/light/{light}',
        json={'on': {'on': on}},
        headers={'hue-application-key': hue_key},
        verify=False,
    )


@app.post('/plex-webhook')
async def root(
        request: fastapi.Request,
        payload: payload.Events = fastapi.Depends(payload.model_from_form),
) -> str:

    if not isinstance(payload, BaseEvent):
        unknown_events = request_data.get('unknown_events', [])
        unknown_events.append(payload)
        request_data['unknown_events'] = unknown_events
        return 'unknown'

    if not request.state.hue_key:
        return 'no key'
    event = payload.event

    match event.split('.'):
        case ['media', command]:
            handle_media_command(command, request.state.hue_key)

    return 'success'


@app.get(
    '/',
    response_class=PrettyJSONResponse,
    response_model=Dict[str, Union[payload.Events, List[Any]]]
)
async def root_get() -> Dict[str, Union[payload.Events, List[Any]]]:
    return request_data

@app.get(
    '/event_schemas',
    response_class=PrettyJSONResponse,
    response_model=Dict[str, Any],
)
async def get_schemas() -> Dict[str, Any]:
    return schema_of(payload.Events, title='Event Schemas')


