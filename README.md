Repository tổng hợp 6 bài tập về background task, queue và worker trong Python/FastAPI.

## Exercises

### Ex1 — FastAPI + BackgroundTasks
FastAPI nhận request, đăng ký worker bằng `BackgroundTasks`, trả response rồi worker tiếp tục xử lý.

[Run & Result](./Ex1/README_Bai1.md)

### Ex2 — asyncio.Queue + Worker
`main()` đưa task vào `asyncio.Queue`, worker lấy task ra xử lý cho đến khi hoàn thành.

[Run & Result](./Ex2/README_Bai2.md)

### Ex3 — FastAPI + asyncio.Queue + Worker
FastAPI nhận request, đưa task vào `asyncio.Queue` và worker lấy task ra để xử lý.

[Run & Result](./Ex3/README_Bai3.md)

### Ex4 — Redis + ARQ + Worker
Producer enqueue job vào Redis, sau đó ARQ Worker lấy job và xử lý.

[Run & Result](./Ex4/README_Bai4.md)

### Ex5 — FastAPI + Redis + ARQ + Worker
FastAPI nhận request, enqueue job vào Redis và ARQ Worker lấy job để xử lý.

[Run & Result](./Ex5/README_Bai5.md)

### Ex6 — FastAPI + Redis + Celery + Worker
FastAPI tạo Celery task, task được đưa vào Redis Broker và Celery Worker lấy task để xử lý.

[Run & Result](./Ex6/README_Bai6.md)
