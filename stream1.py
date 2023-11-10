import asyncio
from fastapi import FastAPI

from fastapi.responses import StreamingResponse

app = FastAPI()


async def stream():
    for i in range(10):
        yield b'{"stream": "100"}\n'
        await asyncio.sleep(1)


@app.get("/stream1")
async def main():
    return StreamingResponse(stream())
