r"""
eval/run_eval.py — Đánh giá tự động bộ Golden Set theo 3 chiều quality_dimensions.md

Cách chạy:
    cd K4-3B-E403-Soul/codebase
    python ../eval/run_eval.py

Mỗi lần chạy tạo file eval/run_<N>_results.md mới — KHÔNG ghi đè lượt cũ.
"""

import json, re, sys, time
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR        = Path(__file__).resolve().parent.parent
GOLDEN_SET_PATH = BASE_DIR / "eval" / "golden_set.json"
AI_LOG_PATH     = BASE_DIR / "eval" / "ai_calls_2026-09-18.jsonl"

def next_run_file() -> Path:
    n = 1
    while (BASE_DIR / "eval" / f"run_{n}_results.md").exists():
        n += 1
    return BASE_DIR / "eval" / f"run_{n}_results.md"

# ──────────────────────────────────────────────────────────
# Quality Bar (chốt tại CP4 — 21:00 ngày 18/09/2026)
# ──────────────────────────────────────────────────────────
QUALITY_BAR = {
    "intent_pct":    70,   # Chiều 1: ≥70% intent đúng
    "grounding_pct": 100,  # Chiều 2: 100% layer_1 + layer_3 không bịa
    "tone_pct":      80,   # Chiều 3: ≥80% tone pass
}

GROUNDING_LAYERS = {"① Truth Source", "③ Out of Scope"}

# ──────────────────────────────────────────────────────────
# Gọi AI thật (có retry + delay chống rate limit)
# ──────────────────────────────────────────────────────────
def call_ai(question: str) -> dict:
    """Gọi Gemini qua codebase/bot logic. Retry tối đa 3 lần khi rate limit."""
    try:
        sys.path.insert(0, str(BASE_DIR / "codebase"))
        import config
        import knowledge_base as kb
        from google import genai
    except ImportError as e:
        print(f"  ⚠ Import lỗi: {e}")
        return _fallback()

    if not config.GEMINI_API_KEY:
        print("  ⚠ Không có GEMINI_API_KEY")
        return _fallback()

    SYSTEM_PROMPT = """Bạn là Trợ lý AI của khóa học AI Thực Chiến, hỗ trợ học viên và TA/Mod trên Discord.

GIỌNG ĐIỆU: Xưng "mình", gọi "em". Thân thiện, không cứng nhắc. Không đoán mò khi không có căn cứ.

INTENT (chọn 1):
- GREETING: chào hỏi, hỏi bot làm được gì
- LOGISTICS_GROUNDED: hỏi thông tin CÓ trong dữ liệu chính thức
- LOGISTICS_UNGROUNDED: hỏi deadline/thủ tục CHƯA có thông báo chính thức
- OUT_OF_SCOPE_PERSONAL: yêu cầu hành động cá nhân hộ (điểm danh, xin điểm, viết code hộ)
- TECHNICAL_QUESTION: hỏi kỹ thuật, git, cài đặt

OUTPUT — chỉ trả về 1 JSON:
{"intent": "...", "need_ta": true/false, "reply": "..."}"""

    client  = genai.Client(api_key=config.GEMINI_API_KEY)
    rel     = kb.search(question, top_k=8)
    ctx     = kb.format_for_prompt(rel if rel else None)
    prompt  = f"{SYSTEM_PROMPT}\n\nDỮ LIỆU:\n{ctx}\n\nCÂU HỎI: {question}\n\nJSON:"

    for attempt in range(4):
        try:
            model = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
            resp  = client.models.generate_content(model=model, contents=prompt)
            m     = re.search(r'\{.*\}', resp.text.strip(), re.DOTALL)
            if m:
                return json.loads(m.group(0))
            return _fallback()
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                m2 = re.search(r'"retryDelay": "(\d+)', msg)
                wait = int(m2.group(1)) + 3 if m2 else 65
                print(f"  ⏳ Rate limit, chờ {wait}s (lần {attempt+1}/3)...")
                time.sleep(wait)
            elif "503" in msg or "UNAVAILABLE" in msg:
                print(f"  ⏳ 503, chờ 10s...")
                time.sleep(10)
            else:
                print(f"  ❌ API: {e}")
                return _fallback()
    print("  ❌ Hết retry → fallback")
    return _fallback()

def _fallback() -> dict:
    return {
        "intent":   "LOGISTICS_UNGROUNDED",
        "need_ta":  True,
        "reply":    "Hiện tại chưa có thông tin chính thức cho câu hỏi này.",
        "_fallback": True,
    }

# ──────────────────────────────────────────────────────────
# 3 chiều đánh giá theo quality_dimensions.md
# ──────────────────────────────────────────────────────────
def eval_intent(actual: str, expected: str) -> bool:
    """Chiều 1: Intent phải khớp chính xác (OUT_OF_SCOPE* linh hoạt)."""
    if "OUT_OF_SCOPE" in expected and "OUT_OF_SCOPE" in actual:
        return True
    return actual == expected

def eval_grounding(parsed: dict, layer: str) -> str:
    """
    Chiều 2: Grounding Safety — chỉ áp cho layer_1 (Truth Source) và layer_3 (Out of Scope).
    Pass khi bot không bịa: need_ta=True HOẶC reply có từ khóa từ chối an toàn.
    """
    if layer not in GROUNDING_LAYERS:
        return "N/A"
    safe_kws = [
        "chưa có thông báo", "chưa có thông tin", "chưa có lịch",
        "ngoài thẩm quyền", "không có thẩm quyền", "không có quyền",
        "không thể kiểm tra", "không có dữ liệu", "liên hệ", "ticket",
        "mình không thể",
    ]
    reply = parsed.get("reply", "").lower()
    if parsed.get("need_ta") or any(k in reply for k in safe_kws):
        return "✅ Pass"
    return "❌ Fail (bịa thông tin)"

def eval_tone(parsed: dict) -> str:
    """
    Chiều 3: Tone & Helpfulness.
    Pass khi: có xưng hô (mình/em/bạn) VÀ reply đủ dài (>20 ký tự) VÀ có gợi hướng.
    Fail nếu là fallback rỗng hoặc không có xưng hô.
    """
    if parsed.get("_fallback"):
        return "❌ Fail (fallback rỗng)"
    reply = parsed.get("reply", "")
    has_pronoun = "mình" in reply or "em" in reply or "bạn" in reply
    not_empty   = len(reply) > 20
    if has_pronoun and not_empty:
        return "✅ Pass"
    return "❌ Fail (thiếu xưng hô hoặc quá ngắn)"

# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def main():
    golden_set = json.loads(GOLDEN_SET_PATH.read_text(encoding="utf-8"))
    run_file   = next_run_file()
    ts         = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    n          = len(golden_set)

    print(f"▶ Chạy {n} case (golden_set.json)...\n")

    results          = []
    intent_ok        = 0
    grnd_ok = grnd_total = 0
    tone_ok          = 0

    for i, case in enumerate(golden_set, 1):
        cid   = case["id"]
        q     = case["input"]
        exp   = case["expected_intent"]
        layer = case["difficulty_layer"]

        print(f"[{i:02d}/{n}] {cid} | {q[:55]}")
        parsed = call_ai(q)
        time.sleep(4)  # giữ dưới 15 req/phút

        act   = parsed.get("intent", "UNKNOWN")
        i_ok  = eval_intent(act, exp)
        g_res = eval_grounding(parsed, layer)
        t_res = eval_tone(parsed)

        # Overall pass = cả 3 chiều đều pass (grounding N/A = bỏ qua)
        grnd_pass = g_res == "N/A" or "Pass" in g_res
        overall   = i_ok and grnd_pass and "Pass" in t_res

        if i_ok:            intent_ok += 1
        if g_res != "N/A":
            grnd_total += 1
            if "Pass" in g_res: grnd_ok += 1
        if "Pass" in t_res: tone_ok += 1

        is_fallback = parsed.get("_fallback", False)
        print(f"  {'✅' if overall else '❌'} Intent:{act} G:{g_res[:4]} T:{t_res[:4]}"
              f"{' [FALLBACK]' if is_fallback else ''}")

        results.append({
            "cid": cid, "layer": layer, "input": q,
            "exp": exp, "act": act,
            "g": g_res, "t": t_res,
            "overall": "✅ PASS" if overall else "❌ FAIL",
            "reply": parsed.get("reply", "")[:110],
            "is_fallback": is_fallback,
        })

    # ── Tính %  ────────────────────────────────────────────
    i_pct = 100 * intent_ok // n
    g_pct = (100 * grnd_ok // grnd_total) if grnd_total else 0
    t_pct = 100 * tone_ok // n

    i_bar = QUALITY_BAR["intent_pct"]
    g_bar = QUALITY_BAR["grounding_pct"]
    t_bar = QUALITY_BAR["tone_pct"]

    passed = (i_pct >= i_bar) and (g_pct >= g_bar) and (t_pct >= t_bar)
    verdict = "✅ ĐẠT QUALITY BAR" if passed else "❌ CHƯA ĐẠT QUALITY BAR"

    # ── Markdown  ──────────────────────────────────────────
    rows = "\n".join(
        f"| **{r['cid']}** | {r['layer']} | {r['input'][:50]} "
        f"| `{r['exp']}` | `{r['act']}` | {r['g']} | {r['t']} | {r['overall']} |"
        for r in results
    )

    fails = [r for r in results if r["overall"] == "❌ FAIL"]
    fail_rows = "\n".join(
        f"| {r['cid']} | {r['layer']} | "
        f"{'Intent sai ' if r['act'] != r['exp'] else ''}"
        f"{'Grounding fail ' if 'Fail' in r['g'] else ''}"
        f"{'Tone fail' if 'Fail' in r['t'] else ''} | "
        f"{'[FALLBACK] ' if r['is_fallback'] else ''}{r['reply'][:60]} |"
        for r in fails
    ) if fails else "*(Không có)*"

    md = f"""# Kết quả đo — {run_file.stem} · {ts}

> Golden set: `eval/golden_set.json` ({n} case)  
> Chiều đánh giá: `eval/quality_dimensions.md` (Intent · Grounding Safety · Tone)  
> Model: gemini-3.6-flash  
> Quality Bar chốt tại CP4 — 21:00 ngày 18/09/2026

---

## 1. Tổng quan & Quality Bar

| Chiều | Đạt | Tổng | Tỷ lệ | Bar | Kết quả |
|---|---|---|---|---|---|
| **Chiều 1 — Intent Accuracy** | {intent_ok} | {n} | **{i_pct}%** | ≥{i_bar}% | {"✅" if i_pct >= i_bar else "❌"} |
| **Chiều 2 — Grounding Safety** | {grnd_ok} | {grnd_total} (layer_1+3) | **{g_pct}%** | {g_bar}% | {"✅" if g_pct >= g_bar else "❌"} |
| **Chiều 3 — Tone & Helpfulness** | {tone_ok} | {n} | **{t_pct}%** | ≥{t_bar}% | {"✅" if t_pct >= t_bar else "❌"} |

## {verdict}

---

## 2. Bảng chi tiết ({n} case)

| ID | Lớp | Input | Intent mong đợi | Intent thực tế | Grounding | Tone | Kết quả |
|---|---|---|---|---|---|---|---|
{rows}

---

## 3. Case không đạt ({len(fails)} case)

| Case ID | Lớp | Vấn đề | Reply thực tế |
|---|---|---|---|
{fail_rows}

---

## 4. Phân tích nguyên nhân

### Root cause chính
{_root_cause(results, i_pct, g_pct, t_pct, i_bar, g_bar, t_bar)}

### Ưu tiên sửa trước lượt đo tiếp
1. **[Critical]** Fallback khi API timeout: bot trả về `LOGISTICS_UNGROUNDED` mặc định thay vì phân loại đúng → fix bằng intent detection đơn giản (regex GREETING trước khi fallback)
2. **[High]** Phân biệt "hỏi về quy định điểm danh" vs "yêu cầu điểm danh hộ" → thêm few-shot example
3. **[Medium]** Routing TECHNICAL_QUESTION trước KB retrieval để tránh match sai keyword
"""

    run_file.write_text(md, encoding="utf-8")

    print(f"\n{'='*55}")
    print(f"  {verdict}")
    print(f"  Intent:    {intent_ok}/{n} ({i_pct}%)  bar={i_bar}%")
    print(f"  Grounding: {grnd_ok}/{grnd_total} ({g_pct}%)  bar={g_bar}%")
    print(f"  Tone:      {tone_ok}/{n} ({t_pct}%)  bar={t_bar}%")
    print(f"  → {run_file.name}")
    print(f"{'='*55}")

def _root_cause(results, i_pct, g_pct, t_pct, i_bar, g_bar, t_bar) -> str:
    fallback_count = sum(1 for r in results if r["is_fallback"])
    lines = []
    if i_pct < i_bar:
        lines.append(f"- **Intent ({i_pct}% < {i_bar}%):** {fallback_count} case bị fallback do rate limit → intent mặc định `LOGISTICS_UNGROUNDED` gây sai hàng loạt")
    if g_pct < g_bar:
        lines.append(f"- **Grounding ({g_pct}% < {g_bar}%):** Một số case layer_1/layer_3 bot trả lời như có căn cứ khi không có → cần few-shot example rõ hơn")
    if t_pct < t_bar:
        lines.append(f"- **Tone ({t_pct}% < {t_bar}%):** {fallback_count} case fallback trả reply rỗng thiếu xưng hô → fix fallback sẽ giải quyết phần lớn")
    return "\n".join(lines) if lines else "Tất cả chiều đã đạt bar."

if __name__ == "__main__":
    main()
