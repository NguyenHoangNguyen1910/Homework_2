*Đánh giá kiến trúc, ưu điểm, nhược điểm và phạm vi áp dụng*

# 1. Kiến trúc của bài

Producer đưa task vào asyncio.Queue trong RAM. Một coroutine worker chạy
liên tục, gọi queue.get(), xử lý task và queue.task_done(). main() có
thể dùng queue.join() để chờ toàn bộ task được hoàn tất.

> Producer main()\
> ↓ queue.put()\
> asyncio.Queue (RAM)\
> ↓ queue.get()\
> Worker coroutine\
> ↓\
> Business logic\
> ↓ queue.task_done()\
> queue.join() được giải phóng khi mọi task đã done

# 2. Ưu điểm

  -----------------------------------------------------------------------
  **Ưu điểm**                         **Ý nghĩa**
  ----------------------------------- -----------------------------------
  Hiểu đúng Producer--Queue--Consumer Đây là kiến trúc nền tảng của hầu
                                      hết hệ thống job queue.

  Tách nơi tạo task và nơi xử lý      Producer không cần gọi trực tiếp
                                      business logic.

  Có buffering                        Producer có thể đưa nhiều task vào
                                      queue, worker xử lý dần.

  Có cơ chế chờ hoàn tất chuẩn        queue.join() dựa trên bộ đếm
                                      unfinished tasks, đáng tin hơn kiểm
                                      tra qsize().

  Dễ thêm nhiều worker coroutine      Có thể tạo nhiều consumer để tăng
                                      concurrency cho I/O-bound task.

  Không cần dịch vụ ngoài             Rất tiện cho học async và chạy thử
                                      local.
  -----------------------------------------------------------------------

# 3. Nhược điểm

  -----------------------------------------------------------------------
  **Nhược điểm**                      **Hệ quả**
  ----------------------------------- -----------------------------------
  Queue chỉ nằm trong RAM             Program dừng là toàn bộ task đang
                                      chờ mất.

  Chỉ trong một process               Process khác hoặc máy khác không
                                      truy cập được queue này.

  Không phải distributed queue        Không có broker bên ngoài để phối
                                      hợp nhiều service.

  Không có retry/job metadata sẵn     Muốn retry, timeout, trạng thái,
                                      lịch chạy phải tự xây.

  Cần quản lý worker lifecycle        Worker thường while True và bị chặn
                                      ở queue.get(); phải cancel/shutdown
                                      đúng cách.

  CPU-bound vẫn không tự nhanh hơn    Asyncio chủ yếu hữu ích khi task có
                                      thời gian chờ I/O; CPU nặng cần
                                      process/thread/GPU strategy khác.
  -----------------------------------------------------------------------

# 4. Điểm kỹ thuật cốt lõi

  -----------------------------------------------------------------------
  **API**                             **Vai trò**
  ----------------------------------- -----------------------------------
  queue.put(item)                     Producer đăng ký một công việc mới.

  queue.get()                         Worker chờ và lấy một công việc.

  queue.task_done()                   Báo rằng task đã lấy ra đã xử lý
                                      xong.

  queue.join()                        Chờ số unfinished tasks trở về 0.

  worker_task.cancel()                Yêu cầu dừng coroutine worker khi
                                      chương trình kết thúc.
  -----------------------------------------------------------------------

# 5. Vì sao tốt hơn gọi worker trực tiếp?

Gọi worker trực tiếp tạo coupling: producer phải đợi hoặc trực tiếp chịu
trách nhiệm thực thi. Queue tạo một lớp trung gian, cho phép producer và
consumer hoạt động độc lập hơn về thời điểm.

# 6. Khi nào nên dùng?

- Ứng dụng đơn process cần pipeline async đơn giản.

- Học cơ chế queue, backpressure, worker lifecycle.

- Các task ngắn và chấp nhận mất khi ứng dụng restart.

# 7. Khi nào không nên dùng?

- Cần task tồn tại qua restart.

- Cần nhiều server/process cùng tiêu thụ queue.

- Cần quan sát, retry và persistence ở mức production.

  -----------------------------------------------------------------------
  **Kết luận ngắn: Kiến trúc queue rõ ràng hơn Bài 1, nhưng vẫn chỉ là
  queue trong RAM và chưa phải hệ thống phân tán.**
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
