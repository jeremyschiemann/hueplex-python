from fastapi import FastAPI

from hueplex.PayloadModels import Payload

app = FastAPI()


@app.post('/')
async def root(payload: Payload) -> str:
    return payload.event


@app.get('/')
async def root_get() -> str:
    return 'hello_world'
