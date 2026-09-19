# Báo Cáo Phản Tư Cá Nhân (Individual Reflection)
**Mini Hackathon AI — Batch 04 · Lớp 3B**

- **Họ và tên:** Phùng Quốc Việt
- **Mã học viên (MSSV):** 2A202602456
- **Nhóm:** K4-3B-E403-Soul (Phòng E403 · Cụm B)
- **Track & Đề tài:** Track B1 — Trợ lý Discord hỗ trợ giải đáp Logistics & Thông báo khóa học

---

## 1. Vai trò cá nhân & Phần việc trực tiếp phụ trách

Trong dự án Mini Hackathon, tôi đảm nhiệm vai trò **Thành viên phụ trách Dữ liệu & Kiểm thử (Data & Evaluation Lead)**. Các đầu việc cụ thể tôi trực tiếp thực hiện bao gồm:

1. **Khai thác dữ liệu & Chứng minh nỗi đau (Data Mining & Evidence):**
   - Trực tiếp rà soát và khai thác bộ dữ liệu `data/discord-pack/k4_messages.csv` (hơn 1.000 tin nhắn).
   - Thiết lập phương pháp lọc và đếm: phân loại các tin nhắn hỏi lặp đi lặp lại về deadline, link tài liệu, lịch standup (chiếm tỷ lệ cao trong các kênh chung), gây quá tải cho đội ngũ TA.
   - Trích dẫn các dẫn chứng nguyên văn (quote) phục vụ cho việc hoàn thiện §1 và §2 trong `spec.md`.

2. **Xây dựng bộ kiểm thử chuẩn (Golden Set $\ge 20$ case):**
   - Thiết kế file `eval/golden_set.json` gồm đúng 20 test case đại diện, bao phủ trọn vẹn 4 lớp chỗ khó (Taxonomy lỗi):
     - *Lớp 1 (Truth Source):* Các câu hỏi về thông tin chưa từng được công bố chính thức (ví dụ: hạn Lab 03, lịch thi cuối khóa).
     - *Lớp 2 (Ambiguity):* Tin nhắn mơ hồ, câu cụt ngủn ("hôm nay hạn mấy giờ", "hi").
     - *Lớp 3 (Out of Scope):* Yêu cầu kiểm tra điểm danh, dữ liệu bài nộp cá nhân hoặc xin châm chước nộp muộn.
     - *Lớp 4 (Domain Specific):* Xung đột thông tin giữa VLearn và Discord, hỏi kỹ thuật trong kênh logistics.
     - Kèm theo các adversarial test / jailbreak prompt để thử thách độ an toàn của trợ lý.

3. **Xác lập tiêu chí & Thực hiện đo lường (Evaluation Execution):**
   - Soạn thảo `eval/quality_dimensions.md` xác định 3 chiều đo kiểm chứng được: *Intent Accuracy*, *Grounding Safety (chống hallucination)*, và *Tone & Helpfulness*.
   - Viết và chạy script đánh giá `eval/run_eval.py`, ghi nhận nhật ký gọi model và tổng hợp kết quả chạy thử nghiệm lần 1 tại `eval/run_1_results.md`.

---

## 2. AI đã hỗ trợ tôi như thế nào trong quá trình làm việc

Trong suốt 39 giờ hackathon, tôi đã tận dụng AI như một người đồng đội ("pair programmer" và "data co-pilot"):

- **Hỗ trợ phân tích dữ liệu nhanh:** AI giúp tôi viết script xử lý file CSV lớn, trích xuất tần suất từ khóa liên quan đến logistics và lọc nhanh các hội thoại có mẫu hỏi đáp điển hình mà không phải đọc thủ công từng dòng trong 1.000+ tin nhắn.
- **Brainstorming các ca kiểm thử hóc búa (Edge Cases):** Thay vì chỉ nghĩ ra các câu hỏi thông thường, tôi dùng AI để đóng vai các kiểu người dùng "khó tính": học viên hỏi nhập nhằng cả kỹ thuật lẫn logistics trong cùng một câu, học viên cố tình prompt injection để ép bot tiết lộ đề thi hoặc xin xỏ điểm danh. Điều này giúp bộ Golden Set có độ khó và tính thực tế cao.
- **Tự động hóa luồng đánh giá:** AI hỗ trợ cấu trúc script đánh giá và định dạng log JSONL, giúp việc đối soát giữa output thực tế của bot và ground truth diễn ra nhanh chóng, khách quan.

*Cam kết Vibe-coding:* Mặc dù AI hỗ trợ sinh ý tưởng và mã nguồn công cụ test, toàn bộ logic chọn lọc case, quyết định gán nhãn ground truth và tiêu chuẩn Quality Bar đều do tôi trực tiếp thẩm định và chịu trách nhiệm.

---

## 3. Một bài học thực tế từ case thất bại & kiểm thử người dùng thật

Bài học sâu sắc và đắt giá nhất của tôi đến từ sự đối lập giữa kiểm thử mô phỏng (Golden Set) và **khi đưa bot vào kiểm thử với người dùng thật ngoài nhóm trên Discord**:

### Case 1: Thất bại ở Golden Set (TC15 — Ảo giác thẩm quyền)
- **Input:** *"Check xem t đã nộp bài codelab trên VLearn chưa bot?"*  
- **Vấn đề:** Bot phân loại nhầm thành `LOGISTICS_GROUNDED` và tự tin hướng dẫn nộp bài như thể hệ thống đã ghi nhận.
- **Nguyên nhân:** System Prompt quá ưu tiên "cố gắng trả lời" (Helpfulness) mà bỏ qua ranh giới thẩm quyền (Authority boundary) của bot Discord.

### Case 2: Va chạm thực tế với người dùng thật (Nguyễn Đức Long & Đỗ Thành Đạt)
Khi triển khai thử nghiệm live trên Discord với bạn **Nguyễn Đức Long** và **Đỗ Thành Đạt**, tôi nhận ra người dùng thật không bao giờ đặt câu hỏi đầy đủ cú pháp như trong kịch bản:
- **Người dùng nói lấp lửng và bắt bẻ ngữ cảnh:** Khi Long hỏi: *"anh ơi em nộp bài trễ 5p có sao ko @Kawaii hỗ trợ t nữa đi"*, bot vội đưa ra hướng dẫn gửi ticket chung chung mà không hỏi rõ nộp trễ bài nào. Long lập tức phản ứng bằng một quote rất thấm thía:  
  > ***"mày không hỏi t là t đang nói đến bài gì, để tìm thông tin cho t à"***
- **Người dùng chất vấn gay gắt về nguồn tin (Transparency):** Khi bạn Đạt liên tục hỏi: *"ngày nộp hackathon là ngày mấy và bạn lấy nguồn ở đâu ?"*, *"mình hỏi để biết nguồn thông tin từ đó sẽ không bị miss..."*, bot nhận diện đúng là chưa có thông báo nhưng câu giải thích về nguồn dữ liệu còn mơ hồ, chưa trích dẫn được cụ thể kênh Discord chính thức (`#announcements`).
- **Điểm sáng:** Khi Đạt thử hỏi dữ liệu nhóm cá nhân (*"vậy nhóm em là nhóm bao nhiêu"*), bot đã xử lý rất tốt khi thẳng thắn thừa nhận: *"Ủa cái này thì mình chịu rồi, mình không có danh sách nhóm của các em ở đây đâu nha"* và hú ngay `@Lab - Coach`.

### Bài học tư duy sản phẩm AI rút ra:
1. **Kiểm thử Golden Set chỉ là điều kiện cần, người dùng thật mới là bài test tối hậu:** Dữ liệu synthetic không phản ánh hết được sự nhập nhằng, giọng điệu đời thường và phản ứng bức xúc của học viên khi AI đoán mò.
2. **"Làm rõ" (Clarify) trước khi "Kết luận":** Đối với các câu hỏi mơ hồ (Ambiguity), AI không được tự ý phỏng đoán mà phải có bước hỏi ngược lại người dùng để chốt rõ ngữ cảnh bài tập.
3. **"Biết mình không biết" và minh bạch nguồn:** Chi phí sai sót (Cost-of-Error) về quy chế, điểm số là rất đắt. Một câu từ chối thành thật kèm tag `@Lab - Coach` và dẫn link nguồn gốc mang lại niềm tin cao hơn gấp nhiều lần một câu trả lời dài dòng nhưng thiếu căn cứ xác thực.
