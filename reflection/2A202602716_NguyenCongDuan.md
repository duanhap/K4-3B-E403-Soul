# Reflection — Nguyễn Công Duẩn · MSSV 2A202602716
Nhóm Soul · Phòng E403 · Lớp 3B · Track B1

---

## 1. Vai trò cá nhân & phần việc trực tiếp phụ trách

Em là đội trưởng, phụ trách quản lý tiến độ toàn bộ 6 checkpoint và là người đảm bảo nhóm nộp đúng hạn từ CP1 đến CP5.

Phần việc cụ thể em trực tiếp làm:
- **spec.md §1–§9:** Viết và hoàn thiện toàn bộ 9 phần spec — từ bằng chứng pain (§1), bảng impact 3 ứng viên (§2), giải pháp tương tự (§3), thiết kế + nguyên tắc HAX/PAIR (§4), 4 lớp chỗ khó + 8 kịch bản (§5), 4 đường đi trải nghiệm (§6), chiều chất lượng + quality bar (§7), phân công (§8), changelog (§9).
- **Điều phối willing users:** Liên hệ và xác nhận 4 willing users đồng ý thử prototype trước CP5.
- **Kịch bản demo:** Chuẩn bị script demo 5 phút cho CP6, bao gồm 1 case chuẩn và 1 case chỗ khó.
- **Form nộp:** Nộp đủ 5 form CP1–CP5 bằng MSSV của em.

---

## 2. AI đã hỗ trợ thế nào trong quá trình làm

Em dùng AI (Kiro/Claude) chủ yếu ở 4 việc:

**Tóm tắt yêu cầu thành PLAN.md để hiểu và chia việc:** Đây là việc đầu tiên em làm khi nhận đề. Em đưa toàn bộ 4 file hướng dẫn (01-challenge-brief, 02-guide, 03-ai-spec-template, 04-rubric) cho AI, yêu cầu tổng hợp thành một file PLAN.md duy nhất có timeline, từng bước cụ thể theo từng giai đoạn, checklist tự kiểm và bảng điểm tham khảo. File này giúp cả nhóm 3 người đọc 1 file thay vì 4 file, biết ngay mốc nào cần làm gì, ai làm gì — tiết kiệm ~1 giờ đọc đề và giảm nhầm lẫn deadline giữa các thành viên.

**Viết và hoàn thiện spec.md:** Dùng AI để draft các phần §1–§9 dựa trên canvas và data đã có, sau đó em review và chỉnh lại phần lý luận (đặc biệt §4 cost-of-error và §5 kịch bản rủi ro).

**Soạn câu hỏi hướng dẫn willing users:** AI đề xuất script phiên 10 phút (Comfort → Context → Task → Observe → Hỏi sau), em điều chỉnh để phù hợp với ngữ cảnh bot Discord của nhóm.

**Chuẩn bị nội dung form CP4:** AI tóm tắt quality bar và phần chưa làm xong thành câu ngắn gọn để điền form — tiết kiệm thời gian khi deadline gấp.

---

## 3. Bài học thực tế từ case thất bại của nhóm

**Bài học từ run_1 (60% Intent, 75% Grounding, 70% Tone — chưa đạt bar):**

Lần đầu chạy golden set, 6/20 case fail không phải do prompt sai mà do **API rate limit** — khi quota hết, bot fallback trả `LOGISTICS_UNGROUNDED` cứng và reply không có xưng hô, kéo tụt cả 3 chiều cùng lúc. Em học được rằng: khi build hệ thống AI, **failure mode của infrastructure** (rate limit, timeout, quota) quan trọng không kém failure mode của model — cần thiết kế fallback có intent detection riêng, không dùng một response mặc định cho tất cả lỗi.

Cụ thể hơn: một fallback tốt không phải "trả về câu cứng khi lỗi" mà phải "phân loại được ít nhất GREETING vs không phải GREETING ngay cả khi không có API" — vì GREETING bị trả về nội dung KB ngẫu nhiên là lỗi tệ nhất về trải nghiệm người dùng.
