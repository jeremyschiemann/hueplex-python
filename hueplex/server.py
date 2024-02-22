import fastapi
from fastapi import FastAPI

from hueplex.payload_models import Payload

app = FastAPI()


@app.post('/plex-webhook')
async def root(payload: Payload = fastapi.Depends(Payload.from_form)) -> str:
    return payload.event


@app.get('/')
async def root_get() -> str:
    return 'hello_world'
