# Bài 4 — Redis + ARQ + Worker

## Logic ngắn

```text
main()
→ enqueue job vào Redis
→ ARQ Worker lấy job từ Redis
→ worker() xử lý job
```

## Cách chạy

Cần mở 3 terminal, 3 terminal trước tiên đều phải truy cập môi trường linux bằng lệnh wsl

### Terminal 1 — Chạy Redis

```bash
wsl
redis-server --port 6379
```

Có thể kiểm tra Redis bằng:

```bash
redis-cli ping
```

### Terminal 2 — Chạy ARQ Worker

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex4
```

```bash
uv run --with arq arq E4_Redis_ARQ_Worker.WorkerSettings
```

### Terminal 3 — Chạy Producer để enqueue job

```bash
wsl
cd /mnt/d/Downloads/Homework/Ex4
```

```bash
uv run --with arq python E4_Redis_ARQ_Worker.py
```

## Kết quả

### Terminal Redis

```text
nguyen2006@MSI:/mnt/d/Downloads/Homework/Ex3$ redis-server --port 6379
5733:C 04 Sep 2026 09:56:11.969 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
5733:C 04 Sep 2026 09:56:11.970 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
5733:C 04 Sep 2026 09:56:11.970 * Redis version=8.0.5, bits=64, commit=00000000, modified=0, pid=5733, just started
5733:C 04 Sep 2026 09:56:11.970 * Configuration loaded
5733:M 04 Sep 2026 09:56:11.970 * monotonic clock: POSIX clock_gettime
                _._                                                  
           _.-``__ ''-._                                             
      _.-``    `.  `_.  ''-._           Redis Open Source            
  .-`` .-```.  ```\/    _.,_ ''-._      8.0.5 (00000000/0) 64 bit
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 5733
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

```

### Terminal Producer

```text
nguyen2006@MSI:/mnt/d/Downloads/Homework/Ex4$ uv run --with arq arq E4_Redis_ARQ_Worker.WorkerSettings
09:58:35: Starting worker for 1 functions: worker
09:58:35: redis_version=8.0.5 mem_usage=1.13M clients_connected=1 db_keys=0
09:59:06:   0.50s → c9ee20d9af3d420f8705090e9af81c20:worker('hello')
Worker started: hello
09:59:06:   0.49s → 297c559d5f0140dd88b23f0b35eb728d:worker('redis')
Worker started: redis
09:59:06:   0.49s → 41dafed9f44e4367a27da056936d29e7:worker('fastapi')
Worker started: fastapi
Worker finished: HELLO
09:59:11:   5.00s ← c9ee20d9af3d420f8705090e9af81c20:worker ● 'HELLO'
Worker finished: REDIS
09:59:11:   5.00s ← 297c559d5f0140dd88b23f0b35eb728d:worker ● 'REDIS'
Worker finished: FASTAPI
09:59:11:   5.00s ← 41dafed9f44e4367a27da056936d29e7:worker ● 'FASTAPI'

```

### Terminal ARQ Worker

```text
nguyen2006@MSI:/mnt/d/Downloads/Homework/Ex4$ uv run --with arq python E4_Redis_ARQ_Worker.py
Jobs queued

```
