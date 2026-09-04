*Đánh giá kiến trúc, ưu điểm, nhược điểm và phạm vi áp dụng*

# 1. Kiến trúc của bài

Bài 3 đưa queue và worker của Bài 2 vào vòng đời một web server. FastAPI
tạo worker ở startup/lifespan; mỗi POST /infer chỉ enqueue dữ liệu và
trả 202; worker chạy độc lập trong event loop của cùng process.

> FastAPI startup\
> ↓ create_task(worker())\
> Worker chờ queue.get()\
> \
> Client → POST /infer\
> ↓\
> FastAPI validate request\
> ↓ queue.put(text)\
> asyncio.Queue (RAM)\
> ↓\
> Worker xử lý\
> \
> FastAPI shutdown → worker_task.cancel()

# 2. Ưu điểm

  -----------------------------------------------------------------------
  **Ưu điểm**                         **Ý nghĩa**
  ----------------------------------- -----------------------------------
  API trả response nhanh              Endpoint không cần đợi business
                                      task hoàn thành.

  Kiến trúc rõ hơn BackgroundTasks    Có queue trung gian và worker sống
                                      lâu xuyên suốt vòng đời app.

  Có buffering giữa HTTP và xử lý     Request có thể đến nhanh hơn tốc độ
                                      xử lý trong một khoảng thời gian.

  Lifecycle rõ ràng                   Startup tạo worker; shutdown hủy
                                      worker.

  Dễ giới hạn concurrency             Số worker coroutine quyết định số
                                      task được xử lý song song.

  Phù hợp prototype                   Không phải cài Redis nhưng mô phỏng
                                      khá đúng producer/consumer của
                                      production.
  -----------------------------------------------------------------------

# 3. Nhược điểm

  -----------------------------------------------------------------------
  **Nhược điểm**                      **Hệ quả**
  ----------------------------------- -----------------------------------
  Queue mất khi app restart           Task đang chờ không durable.

  Queue gắn với từng process Uvicorn  Nếu chạy nhiều Uvicorn workers thì
                                      mỗi process có một queue riêng;
                                      request phân bố không đảm bảo vào
                                      cùng queue.

  Không scale worker độc lập          Muốn thêm consumer thường phải thay
                                      cấu trúc app hoặc tăng process web.

  Không có persistence/retry chuẩn    Job thất bại cần tự thiết kế xử lý.

  Rủi ro overload RAM                 Nếu request vào nhanh hơn worker
                                      lâu dài, queue có thể phình to nếu
                                      không đặt maxsize/backpressure.

  Shutdown cần cẩn thận               Cancel ngay có thể làm task đang xử
                                      lý bị ngắt nếu không có graceful
                                      shutdown.
  -----------------------------------------------------------------------

# 4. Cải thiện so với Bài 2

  -----------------------------------------------------------------------
  **Bài 2**                           **Bài 3**
  ----------------------------------- -----------------------------------
  Producer là main() trong script     Producer là HTTP endpoint thực tế.

  Worker được tạo trong main()        Worker gắn với application
                                      lifespan.

  Không có client/server              Có request/response, validation và
                                      status code.

  Queue dùng để học cơ chế            Queue trở thành một phần kiến trúc
                                      server.
  -----------------------------------------------------------------------

# 5. Rủi ro production quan trọng

- Nhiều Uvicorn worker = nhiều bộ nhớ độc lập = nhiều queue độc lập.

- Không nên coi queue RAM là nơi lưu job quan trọng.

- Nên đặt queue maxsize hoặc chiến lược từ chối/giảm tải nếu có nguy cơ
  burst traffic.

- Cần graceful shutdown nếu muốn hoàn tất task đang chạy trước khi dừng
  app.

# 6. Khi nào nên dùng?

- Prototype hoặc internal service đơn process.

- Task I/O nhẹ, không yêu cầu durability.

- Muốn học cách kết hợp application lifecycle + queue + worker.

# 7. Bước nâng cấp tự nhiên

> FastAPI + asyncio.Queue\
> ↓ tách queue ra khỏi RAM\
> Redis broker\
> ↓ tách worker khỏi web process\
> ARQ Worker / Celery Worker

  -----------------------------------------------------------------------
  **Kết luận ngắn: Bài 3 là cầu nối từ async queue trong một script sang
  kiến trúc web thực tế, nhưng điểm yếu lớn nhất vẫn là queue trong RAM
  và cùng process.**
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
