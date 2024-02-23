import json
from typing import Dict, Any, Union, List, get_args, Mapping

import fastapi
import pydantic
from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import schema_of, schema_json_of, Json
from starlette.background import BackgroundTask

from hueplex import payload
from hueplex.models.base import BaseEvent

app = FastAPI()

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
@app.exception_handler(pydantic.ValidationError)
async def handle_validation_error(request: fastapi.Request, exc: fastapi.exceptions.RequestValidationError | pydantic.ValidationError):

    errors = request_data.get('errors', [])
    errors.append(
        {
            'body': exc.body if isinstance(exc, fastapi.exceptions.RequestValidationError) else str(exc),
            'detail': exc.errors(),
        },
    )
    request_data['errors'] = errors

    return request_validation_exception_handler(request, exc)



@app.post('/plex-webhook')
async def root(payload: payload.Events = fastapi.Depends(payload.model_from_form)) -> str:

    if isinstance(payload, BaseEvent):
        request_data[payload.event] = payload
    else:
        unknown_events = request_data.get('unknown_events', [])
        unknown_events.append(payload)
        request_data['unknown_events'] = unknown_events
    return 'success'


@app.get(
    '/',
    response_model=Dict[str, Union[payload.Events, List[Any]]]
)
async def root_get() -> Dict[str, Union[payload.Events, List[Any]]]:
    return request_data


@app.get(
    '/event_schemas',
    response_class=PrettyJSONResponse
)
async def get_schemas():
    return schema_of(payload.Events, title='Event Schemas')


