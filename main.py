import asyncio

import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTasks

client = httpx.AsyncClient()

app = FastAPI()


def merge_async_iters(*aiters):
    queue = asyncio.Queue(1)
    run_count = len(aiters)
    cancelling = False

    async def drain(aiter):
        nonlocal run_count
        try:
            async for item in aiter:
                await queue.put((False, item))
        except Exception as e:
            if not cancelling:
                await queue.put((True, e))
            else:
                raise
        finally:
            run_count -= 1

    async def merged():
        try:
            while run_count:
                raised, next_item = await queue.get()
                if raised:
                    cancel_tasks()
                    raise next_item
                yield next_item
        finally:
            cancel_tasks()

    def cancel_tasks():
        nonlocal cancelling
        cancelling = True
        for t in tasks:
            t.cancel()

    tasks = [asyncio.create_task(drain(aiter)) for aiter in aiters]
    return merged()


@app.get("/main")
async def main():
    req1 = client.build_request("GET", "http://localhost:8001/stream1")
    r1 = await client.send(req1, stream=True)

    req2 = client.build_request("GET", "http://localhost:8002/stream2")
    r2 = await client.send(req2, stream=True)

    background = BackgroundTasks()
    background.add_task(r1.aclose)
    background.add_task(r2.aclose)

    return StreamingResponse(
        merge_async_iters(
            r1.aiter_text(),
            r2.aiter_text(),
        ),
        background=background
    )
