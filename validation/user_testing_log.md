# NHẬT KÝ KIỂM THỬ NGƯỜI DÙNG (USER TESTING LOG) — KHỐI R6

> **Mục đích:** Đánh giá hiệu quả thực tế của giải pháp Tối ưu Trợ lý Discord (Track B1) khi người dùng thật bên ngoài nhóm thao tác.  
> **Thời gian thực hiện:** Ngày 18/09/2026  
> **Phiên bản thử nghiệm:** Prototype Bot Discord v1.0 (kèm Thinking UI Button) & Web Demo Stepper.

---

## 1. Danh sách người tham gia thử nghiệm (≥ 5 người)

| STT | Họ và tên | MSSV | Lớp / Phòng | Phân loại | Trạng thái |
| :---: | :--- | :---: | :---: | :--- | :---: |
| 1 | **Thái Phúc Tiến** | 2A202602873 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 2 | **Trần Đình Duy** | 2A202602631 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 3 | **Nguyễn Thành Luân** | 2A202602769 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 4 | **Nguyễn Đức Long** | 2A202602917 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 5 | **Chu Thùy Dương** | 2A202602660 | Lớp 3B · E403 | Học viên cùng lớp ngoài nhóm | Đã hoàn thành |

---

## 2. Bảng nhật ký trải nghiệm chi tiết (User Testing Log)

| Người thử | Nhiệm vụ (Task) giao cho thử | Kẹt ở đâu / Điểm vướng | Quote nguyên văn (Verbatim Quote) | Quyết định của nhóm |
| :--- | :--- | :--- | :--- | :--- |
| **Thái Phúc Tiến**<br>*(Discord: tôm chiên xù)<br>Willing User CP1* | Tra cứu lịch trình các mốc Checkpoint Mini Hackathon hôm nay của lớp 3B. | Bot phản hồi nhanh, giọng điệu thân thiện, có nút Thinking. Tuy nhiên **bot bị lỗi gom Checkpoint theo ngày**: gộp (19:30 & 21:00) thành CP1, gộp cả 3 mốc (16:00, 21:00, 22:30) thành CP2, và gọi mốc thuyết trình là CP3 (thực tế là CP6). Người dùng tưởng đúng và khen xã giao, bot nhận diện lời khen như câu chào mở đầu mới. | Quote 1: *"cho tôi biết lịch mini-hackathon hôm nay của lớp 3b"*<br><br>Quote 2: *"uầy, kawaii chuẩn thế"* | **Sửa ngay trước demo:**<br>1. Chuẩn hóa lại Knowledge Base: Tách rời rành mạch từng mốc độc lập từ CP1 đến CP6, tuyệt đối không gom theo ngày để tránh học viên nhầm hạn nộp.<br>2. Thêm xử lý phân loại Intent: Phản hồi lời khen ngắn gọn lịch sự thay vì reset lại câu chào *"Hi em! Mình luôn sẵn sàng..."*. |
| **Trần Đình Duy**<br>*(Willing User)* | Hỏi xin xem lại điểm lab cá nhân và hỏi về tài khoản Pro của khóa học. | Bot nhận diện là OUT_OF_SCOPE và từ chối, nhưng không hướng dẫn Duy phải liên hệ với ai tiếp theo. | *"Tui hỏi xin lại tk Pro để làm lab mà bot kêu ngoài phạm vi xong nín luôn, rồi giờ tui hỏi ai?"* | **Sửa ngay:** Bổ sung logic phân loại: các thắc mắc về tài khoản/quyền truy cập nội bộ khóa học được chuyển thành `TECH_SUPPORT` hoặc `LOGISTICS_GROUNDED` để tự động tag `@TA` hỗ trợ cấp lại. |
| **Nguyễn Thành Luân**<br>*(Willing User)* | Nhập câu hỏi kỹ thuật: *"Em chạy pip install google-genai bị lỗi OOM CUDA"* | Bot tag `@TA` rất nhanh nhưng câu gợi ý xử lý kỹ thuật ban đầu hơi ngắn (chỉ 1 dòng). | *"Nó tag TA rồi nhưng giá mà mách nước sơ sơ 1-2 cách fix trước thì đỡ phải ngồi đợi TA rep."* | **Giữ nguyên có giải trình:** Thiết kế ưu tiên độ an toàn (Cost-of-error), không phỏng đoán mã lỗi sâu để tránh học viên làm hỏng môi trường máy; bot chỉ tóm tắt 1 dòng nguyên nhân chính rồi bàn giao cho TA. |
| **Nguyễn Đức Long**<br>*(Willing User)* | Hỏi câu hỏi lấp lửng: *"anh ơi em nộp bài trễ 5p có sao ko"* | Bot báo hạn nộp chung của Lab mà không nói rõ chính sách nộp trễ có bị trừ điểm hay không. | *"Tui hỏi việc nộp trễ bị phạt sao mà nó cứ nhắc lại cái deadline hôm qua làm tui hoang mang thêm."* | **Sửa ngay:** Bổ sung vào Knowledge Base quy định cụ thể: *Hạn chót 23:59 Chủ Nhật, sau giờ này form đóng tự động, không chấp nhận nộp bù*. Nếu hỏi tình huống ngoại lệ -> Chuyển ngay cho TA phê duyệt. |
| **Chu Thùy Dương**<br>*(Học viên ngoài nhóm)* | Thử thách hỏi lạc đề: *"Cho hỏi thời tiết Hà Nội hôm nay thế nào"* và spam 3 câu liên tiếp. | Bot từ chối lịch sự, không bị hallucination. Tuy nhiên bot phản hồi hơi chậm (~2.5s) do phải gọi API Gemini. | *"Bot ko bị lừa, rep chuẩn. Nhưng lúc gửi tin nhắn thấy chờ 2-3s mới hiện chữ, tưởng bot bị đơ."* | **Sửa ngay:** Thêm trạng thái `async with message.channel.typing()` trên Discord (bot đang gõ...) để người dùng biết hệ thống đang xử lý, không cảm giác bị đơ. |

---

## 3. Tổng kết 4 dòng bắt buộc (Synthesis & Decisions)

1. **Chủ đề lặp nhiều nhất:**  
   Người dùng rất thích câu trả lời ngắn gọn (≤2 câu) không bị ngập chữ như bot cũ M17171, nhưng băn khoăn về độ tin cậy và cần biết hành động tiếp theo khi bot từ chối trả lời hoặc khi gặp trường hợp đặc biệt (nộp trễ, tài khoản).
2. **Sẽ sửa gì trước demo (trước CP6):**  
   - **Fix lỗi gom Checkpoint:** Cập nhật system prompt yêu cầu AI giữ nguyên số thứ tự từng mốc từ CP1 đến CP6 theo đúng Knowledge Base, tuyệt đối không tự ý gom theo ngày khiến sai lệch tên gọi mốc.  
   - Bật hiệu ứng `typing indicator` ("Bot đang gõ...") và làm nổi bật nút `🧠 Xem suy nghĩ của AI (Căn cứ)`.  
   - Cập nhật prompt và KB bổ sung quy định nộp trễ & tài khoản khóa học, ghi nhận toàn bộ vào **§9 Changelog** trong `spec.md`.
3. **Giữ nguyên gì và vì sao:**  
   - Giữ nguyên nguyên tắc **không tự động tư vấn fix lỗi code phức tạp**: Bot chỉ nêu gợi ý ngắn 1 dòng và tag ngay `@TA`. Lý do: Chi phí sai sót kỹ thuật làm hỏng môi trường code của học viên rất đắt, cần con người kiểm soát.
4. **Cái gì để dành sau hackathon:**  
   - Tính năng tự động tra cứu điểm danh/trạng thái nộp bài cá nhân qua API bot kết nối trực tiếp với Google Sheet / Database điểm của ban tổ chức.
