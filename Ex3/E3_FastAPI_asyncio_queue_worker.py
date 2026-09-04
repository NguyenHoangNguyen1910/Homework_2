import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel


queue = asyncio.Queue()


class InferRequest(BaseModel):
    text: str


async def worker():
    while True:
        task = await queue.get()

        try:
            print(f"Worker started: {task}")

            # Giả lập model inference mất 10 giây
            await asyncio.sleep(10)

            result = task.upper()

            print(f"Worker finished: {result}")

        finally:
            queue.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):

    worker_task = asyncio.create_task(worker())

    yield

    worker_task.cancel()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {
        "status": "alive"
    }


@app.get("/ready")
async def ready():
    return {
        "status": "ready"
    }


@app.post("/infer", status_code=202)
async def infer(data: InferRequest):

    await queue.put(data.text)

    return {
        "status": "queued"
    }