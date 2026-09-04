import time

from celery import Celery


celery_app = Celery(
    "tasks",

    # Redis dùng làm queue
    broker="redis://localhost:6379/0",

    # Redis lưu kết quả
    backend="redis://localhost:6379/1"
)


celery_app.conf.task_track_started = True


@celery_app.task(name="worker")
def worker(text: str):

    print(f"Worker started: {text}")

    # Giả lập công việc nặng
    time.sleep(5)

    result = text.upper()

    print(f"Worker finished: {result}")

    return result