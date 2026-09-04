# Bài 1 — FastAPI + BackgroundTasks

## Logic ngắn

```text
Client gửi request
→ FastAPI nhận request
→ đăng ký worker bằng BackgroundTasks
→ FastAPI trả response
→ worker tiếp tục xử lý
```

## Cách chạy

### Terminal 1 — Chạy FastAPI


```bash
wsl
cd /mnt/d/Downloads/Homework/Ex1
```

```bash
uv run --with fastapi --with uvicorn uvicorn E1_BackgroundTasks:app --reload
```

### Terminal 2 — Gửi request

```bash
wsl
curl -X POST http://127.0.0.1:8000/job   -H "Content-Type: application/json"   -d '{"text":"hello"}'
```

## Kết quả

### Response

```text

{"Status":"Checked"}
```

### Terminal FastAPI

```text
Bat dau lam viec

Sau 10 giây

Da xu ly xong : HELLO
```
