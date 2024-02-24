import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Any, Union, List

import fastapi
import pydantic
from fastapi import FastAPI
import requests
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import schema_of
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from hueplex import payload
from hueplex.models.base import BaseEvent
import yaml

from hueplex.models.media import MediaEvent


@asynccontextmanager
async def lifespan(app: FastAPI):

    root_path = Path(__file__).parent.parent

    with open(root_path / 'action_config.yaml') as f:
        content = yaml.safe_load(f)

    bridge_ip = requests.get('https://discovery.meethue.com/').json()[0]['internalipaddress']

    yield {
        'hue_key': os.getenv('HUE_KEY', None),
        'config': content,
        'bridge_ip': bridge_ip,
    }



app = FastAPI(
    title='Hue Plex',
    lifespan=lifespan,
)

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



def handle_media_command(command: Dict[str, Any], hue_key: str):

    res = requests.get(
        f'https://192.168.1.11/clip/v2/resource/grouped_light',
        headers={'hue-application-key': hue_key},
        verify=False,
    )

    group = [group for group in res.json()['data'] if group['owner']['rid'] == command['zone']][0]

    requests.put(
        f'https://192.168.1.11/clip/v2/resource/grouped_light/{group["id"]}',
        json=command['command'],
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

    for action in request.state.config['actions']:
        payload: MediaEvent
        conditions = (
            action['plex']['event'] == payload.event,
            action['plex']['Player']['title'] == payload.player.title,
            action['plex']['Account']['title'] == payload.account.title,
            action['plex']['Metadata']['type'] == payload.metadata.type,
        )
        if all(conditions):
            handle_media_command(action['hue'], request.state.hue_key)

    return 'success'


@app.get(
    '/req',
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


app.mount('/static', StaticFiles(directory='static'), 'static')

templates = Jinja2Templates(directory="templates")

@app.get(
    '/',
    response_class=fastapi.responses.HTMLResponse,
)
def root(request: fastapi.Request):

    res = requests.get(
        f'https://{request.state.bridge_ip}/clip/v2/resource',
        headers={'hue-application-key': request.state.hue_key},
        verify=False,
    )
    all_resource = res.json()['data']
    data_types = {}
    for resource in all_resource:
        l = data_types.get(resource['type'], [])
        l.append(resource)
        data_types[resource['type']] = l

    app:fastapi.FastAPI = request.app
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'app_name': app.openapi()['info']['title'],
            'resources': data_types,
        },
    )

@app.get(
    '/clicked',
    response_class=fastapi.responses.PlainTextResponse,
)
def clicked(request: fastapi.Request):
    return 'clicked it!'