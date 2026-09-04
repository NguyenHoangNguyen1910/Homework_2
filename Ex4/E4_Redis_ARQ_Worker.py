import asyncio
from arq import create_pool
from arq.connections import RedisSettings


REDIS_SETTINGS = RedisSettings(
    host="localhost",
    port=6379
)


async def worker(ctx, text: str):  
    print(f"Worker started: {text}")

    # Giả lập model inference mất 5 giây
    await asyncio.sleep(5)

    result = text.upper()

    print(f"Worker finished: {result}")

    return result


async def main():
    redis = await create_pool(REDIS_SETTINGS)

    await redis.enqueue_job(
        "worker",
        "hello"
    )

    await redis.enqueue_job(
        "worker",
        "fastapi"
    )

    await redis.enqueue_job(
        "worker",
        "redis"
    )

    print("Jobs queued")


class WorkerSettings:
    functions = [worker]
    redis_settings = REDIS_SETTINGS


if __name__ == "__main__":
    asyncio.run(main())