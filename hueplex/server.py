import json
from typing import Dict, Any

import fastapi
from fastapi import FastAPI

from hueplex.payload_models import Payload

app = FastAPI()

request_data = {}


@app.post('/plex-webhook')
async def root(payload: str = fastapi.Form(...)) -> str:
    data = json.loads(payload)
    request_data[data['event']] = data
    return 'success'



@app.get('/')
async def root_get() -> Dict[str, Any]:
    return request_data
