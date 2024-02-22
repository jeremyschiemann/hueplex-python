import uvicorn

from hueplex.server import app

if __name__ == '__main__':

    uvicorn.run(
        app='hueplex.server:app',
        reload=True,
    )