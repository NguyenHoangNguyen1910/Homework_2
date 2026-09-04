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

Sau khi nhận `task_id`, kiểm tra kết quả:

```bash
curl "http://127.0.0.1:8000/result/<task_id>"
```

## Kết quả

### Terminal Redis

```text
nguyen2006@MSI:/mnt/c/Users/ADMIN$ redis-server --port 6379
6789:C 04 Sep 2026 10:20:28.136 # WARNING Memory overcommit must be enabled!
6789:C 04 Sep 2026 10:20:28.136 * Redis is starting
6789:C 04 Sep 2026 10:20:28.136 * Redis version=8.0.5
6789:M 04 Sep 2026 10:20:28.138 # Warning: Could not create server TCP listening socket *:6379: bind: Address already in use
6789:M 04 Sep 2026 10:20:28.138 # Failed listening on port 6379 (tcp), aborting.

nguyen2006@MSI:/mnt/c/Users/ADMIN$ redis-cli ping
PONG
```

Redis đã chạy sẵn trên port `6379`, nên khi chạy thêm `redis-server --port 6379` sẽ báo `Address already in use`.

---

### Terminal Celery Worker

```text
-------------- celery@MSI v5.6.3 (recovery)
--- ***** -----
-- ******* ---- Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.43
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         tasks
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/1
- *** --- * --- .> concurrency: 20 (prefork)
-- ******* ---- .> task events: OFF
--- ***** -----
-------------- [queues]
                .> celery           exchange=celery(direct) key=celery

[tasks]
  . worker

[2026-09-04 10:19:24,561: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-09-04 10:19:25,575: INFO/MainProcess] mingle: all alone
[2026-09-04 10:19:25,609: INFO/MainProcess] celery@MSI ready.

[2026-09-04 10:22:55,653: INFO/MainProcess] Task worker[150e38f8-6846-4492-a678-19351fb2b922] received
[2026-09-04 10:22:55,663: WARNING/ForkPoolWorker-15] Worker started: hello celery
[2026-09-04 10:23:00,663: WARNING/ForkPoolWorker-15] Worker finished: HELLO CELERY
[2026-09-04 10:23:00,665: INFO/ForkPoolWorker-15] Task worker[150e38f8-6846-4492-a678-19351fb2b922] succeeded in 5.009490049000306s: 'HELLO CELERY'
```

---

### Terminal FastAPI

```text
WARNING:  StatReload detected changes in 'main.py'. Reloading...
INFO:     Started server process [6964]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:41026 - "POST /infer HTTP/1.1" 202 Accepted
```

---

### Response POST `/infer`

```json
{
  "status": "queued",
  "task_id": "150e38f8-6846-4492-a678-19351fb2b922"
}
```

---

### Response GET `/result/{task_id}`

```text
{"status":"SUCCESS","result":"HELLO CELERY"}
```
