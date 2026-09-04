# Bài 5 — FastAPI + Redis + ARQ + Worker

## Logic ngắn

```text
Client
→ FastAPI
→ enqueue job vào Redis
→ ARQ Worker lấy job
→ worker() xử lý
```

```text
max_jobs = 1
→ Worker chỉ xử lý tối đa 1 job cùng lúc
```

## Cách chạy

Cần mở 4 terminal để dễ quan sát.

### Terminal 1 — Chạy Redis

```bash
wsl
redis-server --port 6379
```

Có thể kiểm tra:

```bash
redis-cli ping
```

### Terminal 2 — Chạy FastAPI

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex5
```

```bash
uv run --with fastapi --with uvicorn --with arq uvicorn E5_FastAPI_Redis_ARQ_Worker:app --reload
```

### Terminal 3 — Chạy ARQ Worker

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex5
```

```bash
uv run --with arq --with fastapi arq E5_FastAPI_Redis_ARQ_Worker.WorkerSettings
```

### Terminal 4 — Test `/health`

```bash
wsl
curl http://127.0.0.1:8000/health
```

### Test `/ready`

```bash
curl http://127.0.0.1:8000/ready
```

### Test `/infer`

```bash
curl -X POST http://127.0.0.1:8000/infer   -H "Content-Type: application/json"   -d '{"text":"hello"}'
```

## Kết quả

### Redis

```text
nguyen2006@MSI:/mnt/c/Users/ADMIN$ redis-server --port 6379
6018:C 04 Sep 2026 10:02:06.046 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
6018:C 04 Sep 2026 10:02:06.046 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
6018:C 04 Sep 2026 10:02:06.046 * Redis version=8.0.5, bits=64, commit=00000000, modified=0, pid=6018, just started
6018:C 04 Sep 2026 10:02:06.046 * Configuration loaded
6018:M 04 Sep 2026 10:02:06.046 * monotonic clock: POSIX clock_gettime
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis Open Source            
  .-`` .-```.  ```\/    _.,_ ''-._      8.0.5 (00000000/0) 64 bit
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 6018
  `-._    `-._  `-./  _.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |           https://redis.io       
  `-._    `-._`-.__.-'_.-'    _.-'                                   
 |`-._`-._    `-.__.-'    _.-'_.-'|                                  
 |    `-._`-._        _.-'_.-'    |                                  
  `-._    `-._`-.__.-'_.-'    _.-'                                   
      `-._    `-.__.-'    _.-'                                       
          `-._        _.-'                                           
              `-.__.-'                              

nguyen2006@MSI:/mnt/c/Users/ADMIN$ redis-cli ping
PONG                 

```

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
{"status":"queued","job_id":"7d17946d1eba4141a7e2baed2a7a945c"}

```

### Terminal ARQ Worker

```text

10:06:02: Starting worker for 1 functions: worker
10:06:02: redis_version=8.0.5 mem_usage=1.15M clients_connected=2 db_keys=6
10:06:02:  52.07s → 7d17946d1eba4141a7e2baed2a7a945c:worker('hello') delayed=52.07s
Worker started: hello
Worker finished: HELLO
10:06:07:   5.00s ← 7d17946d1eba4141a7e2baed2a7a945c:worker ● 'HELLO'

```
