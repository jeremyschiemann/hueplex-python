from fastapi import FastAPI, Request
import json



app = FastAPI()


@app.post('/')
async def root(request: Request) -> bytes:

    print(await request.body())

    return b""


@app.get('/')
async def root_get() -> str:
    return 'hello_world'
