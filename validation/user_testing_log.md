# NHẬT KÝ KIỂM THỬ NGƯỜI DÙNG (USER TESTING LOG) — KHỐI R6

> **Mục đích:** Đánh giá hiệu quả thực tế của giải pháp Tối ưu Trợ lý Discord (Track B1) khi người dùng thật bên ngoài nhóm thao tác.  
> **Thời gian thực hiện:** Ngày 18/09/2026  
> **Phiên bản thử nghiệm:** Prototype Bot Discord v1.0 (kèm Thinking UI Button) & Bot Discord Kawaii Live.

---

## 1. Danh sách người tham gia thử nghiệm (≥ 5 người)

| STT | Họ và tên | MSSV | Lớp / Phòng | Phân loại | Trạng thái |
| :---: | :--- | :---: | :---: | :--- | :--- : |
| 1 | **Thái Phúc Tiến** | 2A202602873 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 2 | **Trần Đình Duy** | 2A202602631 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 3 | **Nguyễn Thành Luân** | 2A202602769 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 4 | **Nguyễn Đức Long** | 2A202602917 | Lớp 3B · E403 | **Willing User (đã khai CP1)** | Đã hoàn thành |
| 5 | **Đỗ Thành Đạt** | 2A202602874 | Lớp 3B · E403 | Học viên ngoài nhóm | Đã hoàn thành |

---

## 2. Bảng nhật ký trải nghiệm chi tiết (User Testing Log)

| Người thử | Nhiệm vụ (Task) giao cho thử | Kẹt ở đâu / Điểm vướng | Quote nguyên văn (Verbatim Quote) | Quyết định của nhóm |
| :--- | :--- | :--- | :--- | :--- |
| **Thái Phúc Tiến**<br>*(Discord: tôm chiên xù)<br>Willing User CP1* | Tra cứu lịch trình các mốc Checkpoint Mini Hackathon hôm nay của lớp 3B. | Bot phản hồi nhanh, giọng điệu thân thiện, có nút Thinking. Tuy nhiên **bot bị lỗi gom Checkpoint theo ngày**: gộp (19:30 & 21:00) thành CP1, gộp cả 3 mốc (16:00, 21:00, 22:30) thành CP2, và gọi mốc thuyết trình là CP3 (thực tế là CP6). Người dùng tưởng đúng và khen xã giao, bot nhận diện lời khen như câu chào mở đầu mới. | Quote 1: *"cho tôi biết lịch mini-hackathon hôm nay của lớp 3b"*<br><br>Quote 2: *"uầy, kawaii chuẩn thế"* | **Sửa ngay trước demo:**<br>1. Chuẩn hóa lại Knowledge Base: Tách rời rành mạch từng mốc độc lập từ CP1 đến CP6, tuyệt đối không gom theo ngày để tránh học viên nhầm hạn nộp.<br>2. Thêm xử lý phân loại Intent: Phản hồi lời khen ngắn gọn lịch sự thay vì reset lại câu chào *"Hi em! Mình luôn sẵn sàng..."*. |
| **Trần Đình Duy**<br>*(Willing User)* | Hỏi xin xem lại điểm lab cá nhân và hỏi về tài khoản Pro của khóa học. | Bot nhận diện là OUT_OF_SCOPE và từ chối, nhưng không hướng dẫn Duy phải liên hệ với ai tiếp theo. | *"Tui hỏi xin lại tk Pro để làm lab mà bot kêu ngoài phạm vi xong nín luôn, rồi giờ tui hỏi ai?"* | **Sửa ngay:** Bổ sung logic phân loại: các thắc mắc về tài khoản/quyền truy cập nội bộ khóa học được chuyển thành `TECH_SUPPORT` hoặc `LOGISTICS_GROUNDED` để tự động tag `@TA` hỗ trợ cấp lại. |
| **Nguyễn Thành Luân**<br>*(Willing User)* | Nhập câu hỏi kỹ thuật: *"Em chạy pip install google-genai bị lỗi OOM CUDA"* | Bot tag `@TA` rất nhanh nhưng câu gợi ý xử lý kỹ thuật ban đầu hơi ngắn (chỉ 1 dòng). | *"Nó tag TA rồi nhưng giá mà mách nước sơ sơ 1-2 cách fix trước thì đỡ phải ngồi đợi TA rep."* | **Giữ nguyên có giải trình:** Thiết kế ưu tiên độ an toàn (Cost-of-error), không phỏng đoán mã lỗi sâu để tránh học viên làm hỏng môi trường máy; bot chỉ tóm tắt 1 dòng nguyên nhân chính rồi bàn giao cho TA. |
| **Nguyễn Đức Long**<br>*(Discord: Nguyễn Đức Long)<br>Willing User CP1* | Thử hỏi về quy chế nộp bài muộn và tình huống phát sinh khi nộp trễ checkpoint. | **Điểm kẹt:** Khi Long hỏi câu lấp lửng *"em nộp bài trễ 5p có sao ko"*, bot vội đưa ra hướng dẫn gửi ticket chung chung mà **không hỏi lại xem Long đang nộp trễ bài tập nào** (Lab hay Checkpoint). Người dùng bức xúc phản hồi vì bot thiếu bước làm rõ ngữ cảnh (clarification). Sau khi Long nói rõ *"nộp trễ cp3 5p"*, bot nhận diện chính xác đây là vấn đề quy chế điểm số và từ chối thẩm quyền, tự động tag `@Lab - Coach` để hỗ trợ. | Quote 1: *"anh ơi em nộp bài trễ 5p có sao ko @Kawaii hỗ trợ t nữa đi"*<br><br>Quote 2 (Điểm vướng): ***"mày không hỏi t là t đang nói đến bài gì, để tìm thông tin cho t à"***<br><br>Quote 3: *"mình nộp trễ cp3 5p thì phải làm sao"* | **Sửa ngay trước demo:**<br>1. **Bổ sung bước Clarify (Hỏi lại khi thiếu thông tin):** Khi input mơ hồ về đối tượng bài tập, bot phải chủ động hỏi lại *"Bạn đang hỏi về bài Lab hay Checkpoint cụ thể nào?"* trước khi đưa ra kết luận.<br>2. **Giữ nguyên cơ chế Escalate:** Việc bot từ chối giải quyết điểm số nộp trễ và tag `@Lab - Coach` là cực kỳ chuẩn xác với ranh giới thẩm quyền (Cost-of-error cao). |
| **Đỗ Thành Đạt**<br>*(Discord: T136-ĐỖ THÀNH ĐẠT-02874)<br>Học viên cùng lớp ngoài nhóm* | Thử thách hỏi dồn dập về quyền hạn, nguồn thông tin và dữ liệu nội bộ nhóm. | **Điểm kẹt:** Đạt chất vấn liên tục về căn cứ thông tin của bot (*"ngày nộp hackathon là ngày mấy và bạn lấy nguồn ở đâu ?"*, *"mình hỏi để biết nguồn thông tin từ đó sẽ không bị miss, hãy trả lời xem bạn có truy cập được vào nguồn nào..."*). Bot trả lời chung chung là "dữ liệu của khóa học AI Thực Chiến" mà không trích dẫn cụ thể tên kênh hay link nguồn. Khi Đạt hỏi dữ liệu riêng tư (*"vậy nhóm em là nhóm bao nhiêu"*), bot xử lý rất tốt: thừa nhận không có danh sách nhóm và hú ngay `@Lab - Coach`. | Quote 1: *"ngày nộp hackathon là ngày mấy và bạn lấy nguồn ở đâu ?"*<br><br>Quote 2 (Chất vấn nguồn): ***"mình hỏi để biết nguồn thông tin từ đó sẽ không bị miss, hãy trả lời xem bạn có truy cập được vào nguồn nào , từ đó lấy các thông tin khóa học này"***<br><br>Quote 3 (Thử dữ liệu cá nhân): ***"vậy nhóm em là nhóm bao nhiêu"*** | **Sửa ngay trước demo:**<br>1. **Tăng cường tính minh bạch nguồn (Grounding Transparency):** Khi người dùng hỏi nguồn, bot phải chỉ đích danh các kênh chính thức: kênh `#announcements`, slide bài giảng hoặc tài liệu Yêu cầu Mini Hackathon.<br>2. **Duy trì phản hồi tự nhiên khi Out-of-Scope:** Câu trả lời *"Ủa cái này thì mình chịu rồi, mình không có danh sách nhóm của các em ở đây đâu nha. Để mình hú mấy bạn TA..."* được người dùng đánh giá rất cao vì thật thà, không bịa đặt và chuyển giao đúng người. |

---

## 3. Tổng kết 4 dòng bắt buộc (Synthesis & Decisions)

1. **Chủ đề lặp nhiều nhất:**  
   Người dùng thật chất vấn rất gắt gao về **tính minh bạch của nguồn tin** (lấy từ đâu, có quyền truy cập vào đâu) và đòi hỏi bot phải có **khả năng làm rõ ngữ cảnh (Clarification)** khi câu hỏi mơ hồ, thay vì vội vã đưa ra câu trả lời phỏng đoán.
2. **Sẽ sửa gì trước demo (trước CP6):**  
   - **Xử lý câu hỏi mơ hồ (Ambiguity):** Bổ sung prompt yêu cầu bot hỏi lại để xác định rõ đối tượng bài tập (như phản hồi của Nguyễn Đức Long: *"mày không hỏi t là t đang nói đến bài gì"*).  
   - **Minh bạch hóa nguồn tin (Grounding):** Chỉ rõ các kênh Discord cụ thể (`#announcements`, `#vlearn-support`) và slide khóa học khi giải thích nguồn thông tin cho học viên (theo phản hồi của Đỗ Thành Đạt).  
   - Bật hiệu ứng `typing indicator` ("Bot đang gõ...") và cập nhật toàn bộ thay đổi vào **§9 Changelog** của `spec.md`.
3. **Giữ nguyên gì và vì sao:**  
   - Giữ nguyên cơ chế **từ chối thẩm quyền và tag `@Lab - Coach`**: Khi gặp câu hỏi về điểm số, nộp trễ (Long) hoặc tra cứu nhóm cá nhân (Đạt), bot dứt khoát không bịa đặt mà chuyển giao cho con người. Đây là hành vi chuẩn mực giúp đạt điểm tối đa ở chiều Grounding Safety.
4. **Cái gì để dành sau hackathon:**  
   - Tính năng tự động đồng bộ danh sách nhóm và điểm danh cá nhân.
