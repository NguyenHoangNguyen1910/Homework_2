import asyncio


queue = asyncio.Queue()


async def worker():
    while True:
        task = await queue.get()

        print(f"Worker started: {task}")

        # Giả lập task nặng / model inference
        await asyncio.sleep(5)

        result = task.upper()

        print(f"Worker finished: {result}")

        queue.task_done()


async def main():
    worker_task = asyncio.create_task(worker())

    await queue.put("hello")
    await queue.put("fastapi")
    await queue.put("worker")

    await queue.join()

    worker_task.cancel()


asyncio.run(main())


