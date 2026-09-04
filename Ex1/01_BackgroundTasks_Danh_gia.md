*Đánh giá kiến trúc, ưu điểm, nhược điểm và phạm vi áp dụng*

# 1. Kiến trúc của bài

API nhận request, đăng ký một hàm xử lý nền bằng BackgroundTasks, trả
HTTP response trước, sau đó tiến trình FastAPI thực thi công việc đã
đăng ký.

> Client → POST /infer\
> ↓\
> FastAPI nhận dữ liệu\
> ↓\
> background_tasks.add_task(worker, text)\
> ↓\
> HTTP 202 Accepted trả về client\
> ↓\
> worker() tiếp tục chạy trong cùng ứng dụng FastAPI

# 2. Ưu điểm

  -----------------------------------------------------------------------
  **Ưu điểm**                         **Ý nghĩa thực tế**
  ----------------------------------- -----------------------------------
  Response nhanh                      Client không phải chờ toàn bộ thời
                                      gian xử lý của worker mới nhận phản
                                      hồi.

  Code rất đơn giản                   Không cần Redis, queue server hay
                                      worker process riêng.

  Phù hợp việc nhỏ sau response       Gửi log, gửi email nhẹ, ghi audit,
                                      xử lý phụ trợ ngắn.

  Ít hạ tầng                          Chỉ cần FastAPI/Uvicorn nên dễ học,
                                      dễ chạy local.

  Tách được request khỏi phần việc    Endpoint tập trung nhận/validate
  phụ                                 request, worker làm phần xử lý sau.
  -----------------------------------------------------------------------

# 3. Nhược điểm

  -----------------------------------------------------------------------
  **Nhược điểm**                      **Hệ quả**
  ----------------------------------- -----------------------------------
  Không durable                       Nếu process FastAPI chết hoặc
                                      restart, task chưa hoàn tất có thể
                                      mất.

  Không có queue độc lập              Không có nơi lưu job bền vững để
                                      worker khác lấy lại.

  Worker vẫn dùng tài nguyên của API  Task nặng có thể làm CPU/RAM của
  process                             web server bị chiếm dụng.

  Khó scale riêng                     Không thể tăng số worker nền độc
                                      lập mà không tăng luôn web process.

  Khó retry / theo dõi trạng thái     Không có sẵn job_id, retry policy,
                                      dead-letter queue hay dashboard.

  Không phù hợp task dài/nặng         Inference lớn, xử lý video, batch
                                      data dài dễ ảnh hưởng request mới.
  -----------------------------------------------------------------------

# 4. Điều quan trọng cần hiểu

- BackgroundTasks không biến FastAPI thành một hệ thống job queue hoàn
  chỉnh.

- HTTP 202 chỉ nói "request đã được chấp nhận để xử lý", không có nghĩa
  công việc đã hoàn thành.

- Worker chạy sau khi response được chuẩn bị/trả, nhưng vẫn gắn với vòng
  đời của ứng dụng FastAPI.

- Đây là bước đầu để hiểu khái niệm "request path" và "background work"
  tách nhau.

# 5. Khi nào nên dùng?

- Task ngắn, không quá quan trọng nếu thất bại.

- Không cần theo dõi trạng thái job chi tiết.

- Không cần chạy worker ở máy/process khác.

- Muốn giảm latency cảm nhận của endpoint với logic phụ trợ nhẹ.

# 6. Khi nào không nên dùng?

- Task có thể mất.

- Task kéo dài hàng chục giây/phút hoặc tiêu tốn CPU/GPU lớn.

- Cần retry, scheduling, nhiều worker, theo dõi trạng thái hoặc phân
  phối qua nhiều máy.

# 7. Hướng nâng cấp

> BackgroundTasks\
> ↓ khi yêu cầu tăng\
> In-memory Queue\
> ↓ cần tách process / durable hơn\
> Redis + ARQ / Celery

  -----------------------------------------------------------------------
  **Kết luận ngắn: Dễ nhất và ít hạ tầng nhất, nhưng độ tin cậy và khả
  năng scale thấp nhất trong 5 bài.**
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
