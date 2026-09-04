# Bài 2 — asyncio.Queue + Worker

## Logic ngắn

```text
main() tạo worker
→ main() đưa task vào Queue
→ worker lấy task bằng queue.get()
→ worker xử lý
→ task_done()
→ queue.join() chờ tất cả task xong
→ cancel worker
```

## Cách chạy

### Terminal

```bash
cd /mnt/d/Downloads/Homework/Ex2
```

```bash
uv run python E2_Queue.py
```

## Kết quả

```text

Worker started: hello
Worker finished: HELLO
Worker started: fastapi
Worker finished: FASTAPI
Worker started: worker
Worker finished: WORKER

```
