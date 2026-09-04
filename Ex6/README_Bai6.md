# Bài 6 — FastAPI + Redis + Celery + Worker

## Logic ngắn

```text
Client gửi request
→ FastAPI tạo Celery task bằng worker.delay()
→ Task được đưa vào Redis Broker
→ FastAPI trả response 202 + task_id
→ Celery Worker lấy task từ Redis và xử lý
→ Kết quả được lưu vào Redis Result Backend
→ Client dùng task_id để kiểm tra kết quả
```

## Cấu trúc file

```text
Ex6/
├── main.py
└── task.py
```

## Cách chạy

### Terminal 1 — Redis

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex6
redis-cli ping
```

Nếu trả về:

```text
PONG
```

thì Redis đã chạy.

Nếu Redis chưa chạy:

```bash
redis-server --port 6379
```

---

### Terminal 2 — Celery Worker

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex6
uv run --with "celery[redis]" celery -A task:celery_app worker --loglevel=INFO
```

---

### Terminal 3 — FastAPI

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex6
uv run --with fastapi --with uvicorn --with "celery[redis]" uvicorn main:app --reload
```

---

### Terminal 4 — Gửi request

```bash
wsl
curl -X POST "http://127.0.0.1:8000/infer" \
-H "Content-Type: application/json" \
-d '{"text":"hello celery"}'
```

FastAPI sẽ trả về `task_id`.

Sau đó dùng `task_id` để kiểm tra kết quả:

```bash
curl "http://127.0.0.1:8000/result/<task_id>"
```

Ví dụ:

```bash
curl "http://127.0.0.1:8000/result/abc123"
```

## Kết quả

### Response POST `/infer`

```text

```

### Terminal Celery Worker

```text

```

### Response GET `/result/{task_id}`

```text

```
