import asyncio
from fastapi import FastAPI

from fastapi.responses import StreamingResponse

app = FastAPI()


async def stream():
    for i in range(6):
        yield b'{"stream": "200"}\n'
        await asyncio.sleep(1)


@app.get("/stream2")
async def main():
    return StreamingResponse(stream())
