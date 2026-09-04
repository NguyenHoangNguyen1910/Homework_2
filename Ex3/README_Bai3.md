# Bài 3 — FastAPI + asyncio.Queue + Worker

## Logic ngắn

```text
FastAPI startup
→ tạo worker

Client gửi POST /infer
→ FastAPI đưa task vào asyncio.Queue
→ FastAPI trả response
→ worker lấy task từ Queue
→ worker xử lý
```

## Cách chạy

### Terminal 1 — Chạy FastAPI

```bash

wsl
cd /mnt/d/Downloads/Homework/Ex3

```

```bash

uv run --with fastapi --with uvicorn uvicorn E3_FastAPI_asyncio_queue_worker:app --reload

```

### Terminal 2 — Test health

```bash

wsl
curl http://127.0.0.1:8000/health

```

### Test ready

```bash

curl http://127.0.0.1:8000/ready

```

### Test infer

```bash

curl -X POST http://127.0.0.1:8000/infer   -H "Content-Type: application/json"   -d '{"text":"hello"}'

```

## Kết quả

### `/health`

```text

{"status":"alive"}

```

### `/ready`

```text

{"status":"ready"}

```

### `/infer`

```text

{"status":"queued"}

```

### Terminal FastAPI / Worker

```text

Worker started: hello
Worker finished: HELLO

```
