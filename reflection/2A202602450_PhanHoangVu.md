# BÀI THU HOẠCH TỰ PHẢN ÁNH (REFLECTION) — CHECKPOINT 1

- **Họ và tên:** Phan Hoàng Vũ
- **Mã số sinh viên (MSSV):** 2A202602450
- **Lớp:** 3B — VinAI AI Thực Chiến K4
- **Dự án:** Trợ lý Discord Soul (Track B · Đề B1: Tối ưu Trợ lý hiện có)

---

## 1. Vai trò cá nhân & Phần việc trực tiếp phụ trách

Trong dự án Trợ lý Discord Soul, em đảm nhận vai trò **Phụ trách Kỹ thuật / Prototype Lead (Codebase & Prompt Engineering)**. Các công việc cụ thể em trực tiếp triển khai bao gồm:

1. **Xây dựng Prototype Bot Discord (`codebase/bot.py`, `codebase/knowledge_base.py`)**:
   - Khởi tạo Discord Bot bằng `discord.py`, thiết kế luồng lắng nghe sự kiện nhắn tin, xử lý UI hiển thị (Embeds phân màu theo Intent và nút bấm xem quy trình suy nghĩ `Thinking UI`).
   - Tách biệt kiến trúc giữa tầng Discord Event Handler (`bot.py`) và tầng truy xuất cơ sở tri thức KB (`knowledge_base.py`).

2. **Thiết kế System Prompt & Intent Router (Gọi API Gemini)**:
   - Viết System Prompt phân loại chính xác 5 dạng Intent: `GREETING`, `LOGISTICS_GROUNDED`, `LOGISTICS_UNGROUNDED`, `OUT_OF_SCOPE_PERSONAL`, `TECHNICAL_QUESTION`.
   - Ép kiểu đầu ra của LLM về định dạng JSON nghiêm ngặt chứa các thông tin: `intent`, `need_ta`, `confidence`, `thinking` (3 bước suy nghĩ: Step 1 Intent, Step 2 Source Check, Step 3 Decision) và `reply`.
   - Thiết kế quy chuẩn giọng điệu bắt buộc: xưng *"mình"*, gọi *"em"* thân thiện, ngắn gọn (≤2-3 câu), tuyệt đối không phỏng đoán deadline khi chưa có thông báo chính thức.

3. **Tích hợp RAG Search & Cơ chế Chuyển giao TA (Escalation)**:
   - Lập trình tìm kiếm ngữ cảnh có căn cứ từ 84 mục trong `knowledge.json` để inject vào prompt, giúp tiết kiệm token và đảm bảo căn cứ chính xác.
   - Triển khai cơ chế tự động tag `@TA` và dẫn đường link kênh `#announcements` khi nhận diện câu hỏi chưa có dữ liệu chính thức hoặc vượt quá thẩm quyền dữ liệu cá nhân.

---

## 2. AI đã hỗ trợ em như thế nào trong quá trình làm việc

AI coding tools (Gemini) đóng vai trò là một "Co-pilot" đắc lực giúp em đẩy nhanh tốc độ hoàn thành prototype:

- **Sinh mã nguồn & Boilerplate nhanh chóng**: Hỗ trợ sinh khung mã nguồn Discord.py, xử lý bất đồng bộ (`async/await`) và tích hợp SDK `google-genai` mới chuẩn xác mà không tốn thời gian tra cứu tài liệu.
- **Xây dựng bộ Parse JSON & Fallback An toàn**: Hỗ trợ viết các biểu thức chính quy Regex (`re.search(r'\{.*\}', raw_text)`) để bóc tách JSON tin cậy từ đầu ra dạng text của LLM, tránh tình trạng sập bot khi AI trả về định dạng dư thừa.
- **Tối ưu hóa Prompt & Giảm Token**: AI hỗ trợ gợi ý cách viết System Prompt cô đọng, cùng thuật toán lọc bớt KB items ít liên quan trước khi gửi cho Gemini, giúp bot phản hồi nhanh dưới 3 giây.

---

## 3. Bài học thực tế từ case thất bại của nhóm

Bài học lớn nhất mà em và nhóm rút ra được nằm ở **Đợt chạy kiểm thử Golden Set 20 case (Run 1)** tại `eval/run_1_results.md`:

- **Sự cố thất bại**: Nhóm bị **trượt cả 3 chiều đánh giá** so với Quality Bar (Intent Accuracy chỉ đạt 60% < 70%, Grounding Safety đạt 75% < 100%, Tone đạt 70% < 80%). Nguyên nhân chính là do khi Gemini API gặp rào cản Rate Limit/Timeout, hàm Fallback cục bộ của em mặc định gán intent `LOGISTICS_UNGROUNDED` với câu trả lời cứng nhắc `"Hiện tại chưa có thông tin..."` thiếu xưng hô mình/em, gây tụt điểm hàng loạt. Đặc biệt ở **Case TC15** (Hỏi tra cứu nộp bài cá nhân), bot bị ảo giác (hallucination) hướng dẫn học viên tự tra VLearn thay vì từ chối và escalate cho TA.
- **Bài học rút ra**: 
  1. *Không được phụ thuộc 100% vào LLM bên ngoài mà không có lớp Guardrail cục bộ*: Cơ chế Fallback khi AI lỗi phải được thiết kế thông minh (nhận diện keyword cơ bản như `hi`, `chào` để trả lại `GREETING`, giữ đúng xưng hô xưng "mình" - gọi "em").
  2. *Cần Few-shot Examples sắc nét cho các case ranh giới*: Cần bổ sung các ví dụ trực quan trong System Prompt để chặn đứng nguy cơ AI trả lời "như thật" với các câu hỏi thuộc thẩm quyền dữ liệu cá nhân (điểm danh/điểm số).
