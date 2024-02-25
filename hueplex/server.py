import os
import socket
from contextlib import asynccontextmanager
from pathlib import Path

import fastapi
import httpx
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from hueplex import hue_api
from hueplex.api import status, hue, plex
import yaml


@asynccontextmanager
async def lifespan(app: FastAPI):

    root_path = Path(__file__).parent.parent

    with open(root_path / 'action_config.yaml') as f:
        content = yaml.safe_load(f)

    templates = Jinja2Templates(directory="templates")

    async with httpx.AsyncClient(verify=False) as http_client:
        hue_discovery = await http_client.get('https://discovery.meethue.com/', timeout=0.5)
        yield {
            'hue_key': os.getenv('HUE_KEY', None),
            'config': content,
            'bridge_ip': hue_discovery.json()[0]['internalipaddress'] if hue_discovery.is_success else None,
            'templates': templates,
            'http_client': http_client,
            'hostname': socket.gethostname(),
            'app_name': app.openapi()['info']['title'],
        }



app = FastAPI(
    title='Hue Plex',
    lifespan=lifespan,
)
app.include_router(status.router)
app.include_router(hue.router)
app.include_router(plex.router)
app.mount('/static', StaticFiles(directory='static'), 'static')


@app.get(
    '/',
    response_class=fastapi.responses.HTMLResponse,
)
async def root(request: fastapi.Request):

    resources = await hue_api.get_all_resources(request.state.http_client, request.state.bridge_ip)

    if resources is None:
        return fastapi.responses.RedirectResponse('/hue')

    data_types = {}
    for resource in resources:
        l = data_types.get(resource['type'], [])
        l.append(resource)
        data_types[resource['type']] = l

    templates: Jinja2Templates = request.state.templates
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'app_name': request.state.app_name,
            'resources': data_types,
        },
    )
