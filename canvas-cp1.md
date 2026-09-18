
# CANVAS 7 DÒNG — CHECKPOINT 1 (CP1)

Track B · Trợ lý Discord | Đề B1: Tối ưu Trợ lý hiện có

| # | Dòng | Nội dung |
| --- | --- | --- |
| 1 | Track + đề | Track B · Trợ lý Discord — Đề B1: Tối ưu bot Trợ lý hiện có (Phân loại intent, trả lời logistics có căn cứ chính thức, biết-mình-không-biết và chuyển TA). |
| 2 | Job executor (ai · đang ở đâu · làm gì) | Học viên khóa học đang ở kênh Discord chung, vừa gõ câu hỏi tìm thông tin thủ tục / logistics (hạn nộp bài, quy cách nộp standup, link nộp bài, xử lý sự cố nộp muộn). |
| 3 | Pain một câu (ai – đang làm gì – vướng đâu – hậu quả) | Khi học viên hỏi thông tin logistics quan trọng, bot "Trợ lý" hiện tại trả lời quá dài dòng (trung bình 486 ký tự, 37.4% số tin dài >500 ký tự) và khi không có căn cứ thì giải thích lan man thay vì tag TA, khiến học viên bỏ sót hạn nộp, hoang mang và phải hỏi lặp lại nhiều lần làm loãng kênh chat. |
| 4 | 1–2 bằng chứng đầu (số + cách đếm + mã hội thoại/tin nhắn, hoặc khảo sát/phỏng vấn có số người) | Phương pháp: Đếm trên toàn bộ 1.092 tin nhắn thật trong file `data/discord-pack/k4_messages.csv` của Khóa 4. Số liệu: Bot gửi 313 tin, trong đó 117 tin dài >500 ký tự (37.4%). Nhiều tin dài từ 700 đến 1.482 ký tự. Bằng chứng thiếu căn cứ nhưng trả lời lan man: Tin M07416 hỏi hạn Lab 02 -> bot M28485 trả lời 847 ký tự lòng vòng không tag TA. Bằng chứng hỏi lặp vì bot dài dòng/không rõ ràng: Cùng câu hỏi quy cách nộp standup bị 4 học viên hỏi 4 lần trong 4 phút (M65121, M72480, M45897, M66116 -> bot M17171 dài 1.482 ký tự). Bằng chứng trả lời ngoài thẩm quyền: M84993 (hỏi kiểm tra nộp bài cá nhân), M40677 (hỏi xin châm chước commit trễ) bot đều không chuyển người có thẩm quyền. |
| 5 | Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả) | Một học viên gõ câu hỏi logistics trên Discord · AI quyết định câu hỏi có căn cứ trong thông báo chính thức hay không · nếu CÓ thì trích xuất câu trả lời ngắn gọn (≤2 câu) kèm link thông báo, nếu KHÔNG (hoặc ngoài thẩm quyền) thì thông báo chưa có dữ liệu và tự động tag @TA hỗ trợ · học viên nhận đúng thông tin trong 3 giây mà không sợ nhầm deadline. |
| 6 | AI tự làm đến đâu + 1 dòng lý do · ≥3 willing users ngoài nhóm | **- Tự làm:** Nhận diện intent logistics, trích xuất câu trả lời ngắn gọn kèm link nguồn khi có trong thông báo chính thức.<br>**- Không tự làm:** Không tự phỏng đoán deadline khi chưa có thông báo; không trả lời các câu hỏi can thiệp dữ liệu cá nhân (điểm danh/điểm số); khi không chắc chắn bắt buộc phải chuyển giao (`@TA`).<br>**- Lý do (Cost-of-Error):** Cung cấp sai hạn nộp khiến học viên bị 0 điểm lab — chi phí sai sót rất đắt nên bot phải áp dụng cơ chế "Conditional" (chỉ tự động khi chắc chắn có nguồn).<br>**- Willing users (Đã liên hệ và nhận lời thử prototype):**<br>1. Thái Phúc Tiến - 2A202602873 - 3B<br>2. Trần Đình Duy - 2A202602631 - 3B<br>3. Nguyễn Thành Luân - 2A202602769 - 3B<br>4. Nguyễn Đức Long - 2A202602917 - 3B |
| 7 | Phân công có tên | - **Nguyễn Công Duẩn (Đội trưởng):** Quản lý tiến độ chung các checkpoint, phụ trách hoàn thiện tài liệu spec.md, điều phối Willing Users, chuẩn bị Slide và kịch bản Demo.<br>- **Phùng Quốc Việt (Thành viên):** Phụ trách Data Mining & Bằng chứng nỗi đau (Pain Evidence) từ dữ liệu K4 (k4_messages.csv), xây dựng bộ kiểm thử Golden Set ≥20 case (eval/) và thực hiện đo lường đánh giá.<br>- **Phan Hoàng Vũ (Thành viên):** Phụ trách Kỹ thuật / Prototype (codebase/), thiết kế System Prompt phân loại intent logistics/out-of-scope, tích hợp API gọi AI thật xử lý trích xuất nguồn và cơ chế tag @TA. |

---

### BẢN DẠNG VĂN BẢN (TEXT)

1. Track + đề:
   Track B · Trợ lý Discord — Đề B1: Tối ưu bot Trợ lý hiện có (Phân loại intent, trả lời logistics có căn cứ chính thức, biết-mình-không-biết và chuyển TA).

2. Job executor:
   Học viên khóa học đang ở kênh Discord chung, vừa gõ câu hỏi tìm thông tin thủ tục / logistics (hạn nộp bài, quy cách nộp standup, link nộp bài, xử lý sự cố nộp muộn).

3. Pain một câu:
   Khi học viên hỏi thông tin logistics quan trọng, bot "Trợ lý" hiện tại trả lời quá dài dòng (trung bình 486 ký tự, 37.4% số tin dài >500 ký tự) và khi không có căn cứ thì giải thích lan man thay vì tag TA, khiến học viên bỏ sót hạn nộp, hoang mang và phải hỏi lặp lại nhiều lần làm loãng kênh chat.

4. Bằng chứng đầu tiên (Chuẩn B - Data Mining có phương pháp kiểm chứng):
   - Phương pháp: Đếm trên toàn bộ 1.092 tin nhắn thật trong file `data/discord-pack/k4_messages.csv` của Khóa 4.
   - Số liệu: Bot gửi 313 tin, trong đó 117 tin dài >500 ký tự (37.4%). Nhiều tin dài từ 700 đến 1.482 ký tự.
   - Bằng chứng thiếu căn cứ nhưng trả lời lan man: Tin M07416 hỏi hạn Lab 02 -> bot M28485 trả lời 847 ký tự lòng vòng không tag TA.
   - Bằng chứng hỏi lặp vì bot dài dòng/không rõ ràng: Cùng câu hỏi quy cách nộp standup bị 4 học viên hỏi 4 lần trong 4 phút (M65121, M72480, M45897, M66116 -> bot M17171 dài 1.482 ký tự).
   - Bằng chứng trả lời ngoài thẩm quyền: M84993 (hỏi kiểm tra nộp bài cá nhân), M40677 (hỏi xin châm chước commit trễ) bot đều không chuyển người có thẩm quyền.
   (Sẽ tiến hành khảo sát phỏng vấn sâu 20 học viên trong lớp trước CP4 để bổ sung log câu hỏi - câu trả lời).

5. Lát cắt MỘT CÂU:
   Một học viên gõ câu hỏi logistics trên Discord · AI quyết định câu hỏi có căn cứ trong thông báo chính thức hay không · nếu CÓ thì trích xuất câu trả lời ngắn gọn (≤2 câu) kèm link thông báo, nếu KHÔNG (hoặc ngoài thẩm quyền) thì thông báo chưa có dữ liệu và tự động tag @TA hỗ trợ · học viên nhận đúng thông tin trong 3 giây mà không sợ nhầm deadline.

6. AI tự làm đến đâu + Lý do + Willing users:
   - Tự làm: Nhận diện intent logistics, trích xuất câu trả lời ngắn gọn kèm link nguồn khi có trong thông báo chính thức.
   - Không tự làm: Không tự phỏng đoán deadline khi chưa có thông báo; không trả lời các câu hỏi can thiệp dữ liệu cá nhân (điểm danh/điểm số); khi không chắc chắn bắt buộc phải chuyển giao (@TA).
   - Lý do (Cost-of-Error): Cung cấp sai hạn nộp khiến học viên bị 0 điểm lab — chi phí sai sót rất đắt nên bot phải áp dụng cơ chế "Conditional" (chỉ tự động khi chắc chắn có nguồn).
   - Willing users (Đã liên hệ và nhận lời thử prototype):
     1. Thái Phúc Tiến - 2A202602873 - 3B
     2. Trần Đình Duy - 2A202602631 - 3B
     3. Nguyễn Thành Luân - 2A202602769 - 3B
     4. Nguyễn Đức Long - 2A202602917 - 3B

7. Phân công có tên:
   - Nguyễn Công Duẩn (Đội trưởng): Quản lý tiến độ chung các checkpoint, phụ trách hoàn thiện tài liệu spec.md, điều phối Willing Users, chuẩn bị Slide và kịch bản Demo.
   - Phùng Quốc Việt (Thành viên): Phụ trách Data Mining & Bằng chứng nỗi đau (Pain Evidence) từ dữ liệu K4 (k4_messages.csv), xây dựng bộ kiểm thử Golden Set ≥20 case (eval/) và thực hiện đo lường đánh giá.
   - Phan Hoàng Vũ (Thành viên): Phụ trách Kỹ thuật / Prototype (codebase/), thiết kế System Prompt phân loại intent logistics/out-of-scope, tích hợp API gọi AI thật xử lý trích xuất nguồn và cơ chế tag @TA.
