# AI SPEC — [Tên lát cắt] · Nhóm T-136 · Zone ____
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Lesson Studio  [ ] D — Học tập thích ứng  [ ] E — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

---

## §1. User & Job

- **Job executor + workflow** (đính kèm worksheet JTBD / ảnh sơ đồ):
  - _Ai là người dùng cụ thể? (không phải "học viên nói chung")_
  - _Họ đang làm việc gì? Quy trình hiện tại của họ là gì?_

- **Core JTBD** (không tên sản phẩm/AI trong câu):
  - _Khi [tình huống], tôi muốn [động lực], để [kết quả]_

- **Problem statement** (KHÔNG chữ AI):
  - _Ai — đang làm gì — vướng đâu — hậu quả gì_

- **Evidence** (chuẩn A và/hoặc B — log đầy đủ trong repo):
  - Số liệu mining / kết quả khảo sát (n = ?, % xác nhận): _____
  - ≥5 quote/ví dụ nguyên văn + nguồn:
    1. "_____" — nguồn: _____
    2. "_____" — nguồn: _____
    3. "_____" — nguồn: _____
    4. "_____" — nguồn: _____
    5. "_____" — nguồn: _____

---

## §2. Impact & quyết định chọn

- **Bảng impact ≥3 ứng viên:**

| Ứng viên | Số người gặp | Tần suất | Mỗi lần tốn gì | Khả thi build? | Chọn? |
|---|---|---|---|---|---|
| Ứng viên 1: _____ | ___ người | ___ lần/tuần | ___ phút | Có / Không | ✅ / ❌ |
| Ứng viên 2: _____ | ___ người | ___ lần/tuần | ___ phút | Có / Không | ✅ / ❌ |
| Ứng viên 3: _____ | ___ người | ___ lần/tuần | ___ phút | Có / Không | ✅ / ❌ |

- **Ứng viên ĐÃ LOẠI + vì sao:**
  - Ứng viên X bị loại vì: _____

- **Ứng viên CHỌN + vì sao (bằng số):**
  - Chọn ứng viên Y vì: _____

---

## §3. Giải pháp tương tự đã nghiên cứu

- **[Sản phẩm 1]:**
  - Flow của họ: _____
  - Đáng học: _____
  - Đáng né: _____
  - Mình khác gì: _____

- **[Sản phẩm 2]:**
  - Flow của họ: _____
  - Đáng học: _____
  - Đáng né: _____
  - Mình khác gì: _____

---

## §4. Thiết kế

- **Lát cắt MỘT CÂU** (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
  > _[Người dùng] cần [Công việc] được [Quyết định AI] giúp [Kết quả]_

- **Non-goals** (≥3 thứ KHÔNG build):
  1. Không build: _____
  2. Không build: _____
  3. Không build: _____

- **Mức prototype nhắm tới:** [ ] Sketch  [ ] Mock  [ ] Working
  - Phần nào mock: _____
  - Phần nào chạy thật: _____

- **Automation:** [ ] Augment  [ ] Conditional  [ ] Automate
  - Lý do theo cost-of-error: _"Sai thì [ai chịu gì], sửa [đắt/rẻ] vì ___"_

### §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR)

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| G10 — Thu hẹp phạm vi khi nghi ngờ | _____ |
| G2 — Làm rõ hệ thống làm tốt đến đâu | _____ |
| G9 — Sửa dễ dàng | _____ |
| G11 — Giải thích vì sao | _____ |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

| # | Lớp | Tình huống cụ thể | Hành vi mong muốn | Nguyên tắc áp |
|---|---|---|---|---|
| 1 | ① Nguồn sự thật | _____ | _____ | _____ |
| 2 | ① Nguồn sự thật | _____ | _____ | _____ |
| 3 | ② Mơ hồ/thiếu TT | _____ | _____ | _____ |
| 4 | ② Mơ hồ/thiếu TT | _____ | _____ | _____ |
| 5 | ③ Ngoài phạm vi | _____ | _____ | _____ |
| 6 | ③ Ngoài phạm vi | _____ | _____ | _____ |
| 7 | ④ Đặc thù domain | _____ | _____ | _____ |
| 8 | ④ Đặc thù domain | _____ | _____ | _____ |

---

## §6. Bốn đường đi của trải nghiệm

- **Happy path** (AI tự tin cao, có căn cứ):
  > _User làm gì → AI trả gì → User thấy gì_

- **Low-confidence (②)** (AI thiếu tự tin, input mơ hồ):
  > _User hỏi mơ hồ → AI hỏi lại / báo không chắc → User làm gì tiếp_

- **Failure / không có căn cứ (①)**:
  > _User hỏi ngoài tài liệu → AI từ chối rõ ràng → Gợi ý user tìm ở đâu_

- **Correction (user sửa)**:
  > _AI trả kết quả → User thấy sai → User sửa thế nào_

- **Khi bị đòi ngoài phạm vi (③)**:
  > _User đòi thứ bot không được làm → Bot từ chối và vẫn hữu ích_

- **Case đặc thù domain (④)**:
  > _Tình huống sai thì học viên mất điểm / học sai → Bot xử lý thế nào_

---

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được:**

| Chiều | Định nghĩa "đạt" | Định nghĩa "không đạt" |
|---|---|---|
| Factuality (có căn cứ) | Mọi thông tin truy được về nguồn | Có thông tin bịa không có nguồn |
| Safety (an toàn) | 100% case nhạy cảm bị từ chối | Bất kỳ case nguy hiểm nào được trả lời |
| Relevance (đúng việc) | Trả lời đúng câu được hỏi | Trả lời lạc đề |

- **Golden set:** ≥20 case — xem file `eval/golden_set.json`

- **Quality bar** *(chốt trước 21:00 ngày 17/9, giữ nguyên sau đó)*:
  > "Đạt khi ≥ ___% case qua bộ golden set, VÀ 100% case ngoài phạm vi bị từ chối an toàn"

- **Kết quả các lượt chạy:**

| Lượt | Ngày/giờ | Tổng case | Đạt | Tỷ lệ | Ghi chú |
|---|---|---|---|---|---|
| Run 1 | _____ | 20 | ___ | ___% | _____ |

---

## §8. Phân công & kế hoạch

- **Phân công có tên:**

| Đầu việc | Thành viên phụ trách |
|---|---|
| Spec & evidence | _____ |
| Prompt engineering | _____ |
| Code / codebase | _____ |
| Golden set / eval | _____ |
| Demo & slide | _____ |

- **Willing users** (≥2 tên — khai từ CP1):
  1. Tên: _____ · Vai trò: _____ · Đã xác nhận: Có/Không
  2. Tên: _____ · Vai trò: _____ · Đã xác nhận: Có/Không

- **Kế hoạch validation:**
  - Ngày thử: _____
  - Task giao cho người thử: _____

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| _____ | _____ | _____ |
