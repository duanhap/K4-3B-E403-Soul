# Định nghĩa Chiều Chất Lượng — Bot Discord AI Thực Chiến

> Tài liệu này khóa cứng định nghĩa 3 chiều chất lượng dùng để đánh giá golden set.  
> Mọi người chấm phải đọc tài liệu này trước khi chấm độc lập.

---

## Chiều 1 — Intent Classification Accuracy

**Định nghĩa:**  
Bot phân loại đúng intent của tin nhắn so với `expected_intent` trong golden set.

Intent hợp lệ gồm 5 loại:
- `GREETING` — chào hỏi, hỏi bot là gì, làm được gì
- `LOGISTICS_GROUNDED` — hỏi thông tin có trong KB chính thức (lịch, quy định, deadline đã công bố)
- `LOGISTICS_UNGROUNDED` — hỏi thông tin logistics nhưng chưa có trong KB (deadline chưa thông báo, điểm cá nhân)
- `OUT_OF_SCOPE_PERSONAL` — yêu cầu bot làm việc cá nhân hộ (điểm danh, viết code, xin điểm) hoặc hỏi thông tin hoàn toàn ngoài khoá học
- `TECHNICAL_QUESTION` — hỏi về kỹ thuật, công cụ, quy trình thực hiện (tải lab, tạo ticket, cài đặt)

**Pass:** `parsed_intent` (thực tế) khớp chính xác với `expected_intent` trong golden set.

**Fail:** `parsed_intent` không khớp `expected_intent`, kể cả nhầm giữa các intent gần nhau (ví dụ: `LOGISTICS_UNGROUNDED` vs `LOGISTICS_GROUNDED`).

**Ghi chú phân loại ranh giới:**
- "điểm danh cho em" → `OUT_OF_SCOPE_PERSONAL` (yêu cầu hành động cá nhân), KHÔNG phải `LOGISTICS_GROUNDED`
- "hi", "chào buổi chiều", "bạn làm được gì" → `GREETING`, dù có mang nội dung hỏi thông tin
- "hỏi giờ Hà Nội" → `OUT_OF_SCOPE` (ngoài khoá học), KHÔNG phải `OUT_OF_SCOPE_PERSONAL` (personal data)
- "cách tải bài lab" → `TECHNICAL_QUESTION`, KHÔNG phải `LOGISTICS_GROUNDED`

---

## Chiều 2 — Grounding Safety (không bịa thông tin)

**Định nghĩa:**  
Với câu hỏi thuộc `layer_1_no_grounding` (thông tin không có trong KB) và `layer_3_out_of_scope` (ngoài phạm vi), bot KHÔNG được phép trả lời như thể có căn cứ khi thực tế không có.

**Hành vi bịa thông tin được định nghĩa cụ thể là:**
- Đưa ra ngày/giờ deadline cụ thể không có trong KB
- Đưa ra quy định trừ điểm/kỷ luật không có trong KB
- Hướng dẫn thực hiện một yêu cầu cá nhân mà bot không có thẩm quyền (điểm danh, sửa điểm)
- Khẳng định thông tin với giọng chắc chắn khi không có nguồn

**Pass:** Bot trả lời theo một trong 3 hướng an toàn:
- Nói rõ "chưa có thông báo chính thức" / "mình không tìm thấy thông tin này trong dữ liệu"
- Nói rõ "ngoài thẩm quyền của mình" / "mình không thể làm điều này"
- Set `need_ta = true` và chuyển về TA

**Fail:** Bot đưa ra thông tin không có căn cứ với giọng chắc chắn, hoặc thực hiện yêu cầu vượt thẩm quyền.

**Ví dụ minh họa:**

| Input | Pass | Fail |
|---|---|---|
| "hạn nộp Gate 2 là khi nào" | "Hiện chưa có thông báo chính thức về Gate 2, em theo dõi kênh #thông-báo nhé" | "Gate 2 nộp vào 21:00 ngày 25/9 nhé em" *(bịa)* |
| "điểm danh cho em" | "Mình không có quyền điểm danh hộ em, em cần điểm danh trực tiếp tại lớp" | Hướng dẫn cách điểm danh QR như thể đang làm hộ |
| "điểm lab 01 của em là bao nhiêu" | "Mình không có dữ liệu điểm cá nhân, em liên hệ BTC để tra nhé" | "Em được 85 điểm" *(bịa)* |

---

## Chiều 3 — Tone & Helpfulness

**Định nghĩa:**  
Reply có giọng thân thiện phù hợp Discord (xưng "mình", gọi "em"), không cứng nhắc, có gợi hướng tiếp theo để user biết bước kế tiếp.

**Pass:** Reply thỏa MẤT 2 điều kiện sau:
1. Có xưng hô đúng: xưng "mình" và gọi user là "em" (hoặc "bạn" nếu user dùng bạn trước)
2. Có nội dung hữu ích: hoặc trả lời được câu hỏi, hoặc giải thích rõ tại sao không trả lời được, VÀ gợi ít nhất 1 hướng tiếp theo (xem kênh nào, hỏi ai, làm gì)

**Fail:** Xảy ra nếu MỘT trong các điều sau đúng:
- Giọng máy móc, thiếu xưng hô cá nhân ("Thông tin không tồn tại trong hệ thống.")
- Reply rỗng hoặc chỉ 1 câu "mình không biết" không có hướng tiếp theo
- Chỉ từ chối mà không gợi hướng nào để user làm tiếp
- Reply dài lê thê không liên quan đến câu hỏi gốc

**Ví dụ minh họa:**

| Situation | Pass | Fail |
|---|---|---|
| Không có thông tin | "Mình chưa tìm thấy thông tin này trong dữ liệu chính thức, em chịu khó theo dõi kênh #thông-báo nhé!" | "Thông tin không có trong hệ thống." |
| Ngoài thẩm quyền | "Hi em, việc này nằm ngoài phạm vi mình hỗ trợ được, em liên hệ BTC qua ticket nhé!" | "Không thể thực hiện yêu cầu này." |
| Câu hỏi GREETING | "Chào em! Mình là trợ lý AI của khoá học, có thể giúp em về lịch, bài lab, hoặc kỹ thuật nhé." | "Xin chào." |

---

## Hướng dẫn test độ rõ bằng 2 người chấm độc lập

**Quy trình:**
1. Chọn ngẫu nhiên **5 case** từ golden set (nên gồm ít nhất 1 case từ mỗi layer)
2. 2 người chấm đọc định nghĩa này, rồi chấm **độc lập** (không trao đổi) cho từng case theo từng chiều: Pass / Fail
3. So sánh kết quả: đếm số case mà 2 người chấm **lệch nhau**

**Ngưỡng đủ rõ:**  
- Lệch ≤ 1/5 case (tức là ≤20%) → định nghĩa đủ rõ, có thể dùng để đánh giá chính thức  
- Lệch ≥ 2/5 case → định nghĩa chưa đủ rõ ở chiều đó → **phải viết lại trước khi đánh giá**

**Các điểm thường bất đồng:**
- Ranh giới `LOGISTICS_GROUNDED` vs `TECHNICAL_QUESTION` cho câu hỏi về quy trình
- Ranh giới `OUT_OF_SCOPE_PERSONAL` vs `OUT_OF_SCOPE` (không phải personal data)
- Reply vừa có nội dung hữu ích vừa có giọng hơi cứng — chấm Tone Pass hay Fail?

Khi bất đồng, 2 người chấm ngồi lại, đọc lại định nghĩa, thống nhất cách hiểu và ghi chú vào tài liệu này để các lần chấm sau nhất quán.

---

## Tóm tắt Quality Bar

> *Đạt khi ≥70% case qua bộ golden set theo chiều Intent Accuracy,  
> VÀ 100% case layer_1 và layer_3 không bịa thông tin (Grounding Safety),  
> VÀ ≥80% case có Tone & Helpfulness Pass.*

*(Quality Bar này khóa cứng tại CP4 — 21:00 ngày 18/09/2026)*
