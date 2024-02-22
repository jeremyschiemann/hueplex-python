from typing import Dict, Any, Union, List

import fastapi
from fastapi import FastAPI
from fastapi.exception_handlers import request_validation_exception_handler

from hueplex import payload_models

app = FastAPI()

request_data = {}


@app.exception_handler(fastapi.exceptions.RequestValidationError)
async def handle_validation_error(request: fastapi.Request, exc: fastapi.exceptions.RequestValidationError):

    errors = request_data.get('errors', [])
    errors.append(
        {
            'body': exc.body,
            'detail': exc.errors(),
        },
    )
    request_data['errors'] = errors

    return request_validation_exception_handler(request, exc)



@app.post('/plex-webhook')
async def root(payload: Any = fastapi.Depends(payload_models.model_from_form)) -> str:

    if isinstance(payload, payload_models.MediaEvent):
        request_data[payload.event] = payload
    else:
        unknown_events = request_data.get('unknown_events', [])
        unknown_events.append(payload)
        request_data['unknown_events'] = unknown_events
    return 'success'


@app.get(
    '/',
    response_model=Dict[str, Union[payload_models.Events, List[Any]]]
)
async def root_get() -> Dict[str, Union[payload_models.Events, List[Any]]]:
    return request_data
