import asyncio
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


redis_settings = RedisSettings(
    host="localhost",
    port=6379
)


class InferRequest(BaseModel):
    text: str


async def worker(ctx, text: str):
    print(f"Worker started: {text}")

    # Giả lập model inference mất 5 giây
    await asyncio.sleep(5)

    result = text.upper()

    print(f"Worker finished: {result}")

    return result


@asynccontextmanager
async def lifespan(app: FastAPI):

    # FastAPI kết nối Redis khi startup
    app.state.redis = await create_pool(redis_settings)

    yield

    # Đóng Redis connection khi shutdown
    await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {
        "status": "alive"
    }


@app.get("/ready")
async def ready(request: Request):
    try:
        await request.app.state.redis.ping()

        return {
            "status": "ready"
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Redis not ready"
        )


@app.post("/infer", status_code=202)
async def infer(
    data: InferRequest,
    request: Request
):

    job = await request.app.state.redis.enqueue_job(
        "worker",
        data.text
    )

    return {
        "status": "queued",
        "job_id": job.job_id
    }


class WorkerSettings:
    functions = [worker]
    redis_settings = redis_settings
    
    # Chỉ chạy 1 job cùng lúc để dễ quan sát
    max_jobs = 1