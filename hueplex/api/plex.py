from typing import Dict, Any

import fastapi
import httpx
from pydantic import schema_of

from hueplex import payload, hue_api
from hueplex.api import status
from hueplex.lib.responses import PrettyJSONResponse
from hueplex.models.base import BaseEvent
from hueplex.models.media import MediaEvent
from hueplex.payload import Events

hooks_received = {}


router = fastapi.APIRouter()


@router.get(
    '/received_hooks',
    response_class=PrettyJSONResponse,
    response_model=Dict[str, Events]
)
async def get_received_hooks():
    return hooks_received

@router.get(
    '/event_schemas',
    response_class=PrettyJSONResponse,
    response_model=Dict[str, Any],
)
async def get_schemas() -> Dict[str, Any]:
    return schema_of(payload.Events, title='Event Schemas')


@router.post('/plex-webhook')
async def plex_webhook(
        request: fastapi.Request,
        payload: payload.Events = fastapi.Depends(payload.model_from_form),
) -> str:

    if not isinstance(payload, BaseEvent):
        unknown_events = hooks_received.get('unknown_events', [])
        unknown_events.append(payload)
        hooks_received['unknown_events'] = unknown_events
        return 'unknown'

    if not status.is_active:
        return 'no active'

    for action in request.state.config['actions']:
        payload: MediaEvent
        if is_contained(action['plex'], payload.model_dump(by_alias=True)):
            await handle_media_command(request.state.http_client, request.state.bridge_ip, action['hue'])

    return 'success'


def is_contained(small: Dict[str, Any], big: Dict[str, Any]):
    for key, value in small.items():
        if key not in big:
            return False
        if isinstance(value, dict):
            if not isinstance(big[key], dict) or not is_contained(value, big[key]):
                return False
        elif value != big[key]:
            return False
    return True



async def handle_media_command(http: httpx.AsyncClient, bridge_ip: str, command: Dict[str, Any]):
    grouped_light = await hue_api.get_grouped_lights(http, bridge_ip)
    group = [group for group in grouped_light if group['owner']['rid'] == command['zone']][0]
    await hue_api.execute_commad(http, bridge_ip, group['id'], command['command'])
