"""
bot.py — Discord Bot Trợ lý (Track B1)

KB logic đã tách sang knowledge_base.py
Bot chỉ xử lý: Discord events · Gemini API call · intent routing · thinking UI
"""

import json
import re
import logging
import datetime
from pathlib import Path

import discord
from discord.ext import commands
from discord.ui import Button, View
from google import genai

import config
import knowledge_base as kb  # ← KB module tách riêng

# ─────────────────────────────────────────────
# Helper: mention kênh #announcements thật
# ─────────────────────────────────────────────
def _announcements_mention() -> str:
    """Trả về <#ID> nếu đã cấu hình, fallback text nếu chưa."""
    cid = getattr(config, "ANNOUNCEMENTS_CHANNEL_ID", "")
    return f"<#{cid}>" if cid else "#announcements"

# ─────────────────────────────────────────────
# Logging setup (cho CP3: lưu mọi AI call)
# ─────────────────────────────────────────────
LOG_DIR = Path(__file__).parent.parent / "eval"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"ai_calls_{datetime.date.today().isoformat()}.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def log_ai_call(case_id: str, user_input: str, prompt: str, raw_output: str, parsed: dict):
    """Ghi log mỗi lần gọi AI vào file JSONL trong eval/ (dùng cho golden set)."""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "case_id": case_id,
        "input": user_input,
        "prompt_length": len(prompt),
        "raw_output": raw_output,
        "parsed_intent": parsed.get("intent"),
        "parsed_need_ta": parsed.get("need_ta"),
        "parsed_confidence": parsed.get("confidence"),
        "parsed_reply": parsed.get("reply"),
    }
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        logging.warning(f"Không ghi được log AI call: {e}")


# ─────────────────────────────────────────────
# Discord + Gemini client
# ─────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ai_client = None
if config.GEMINI_API_KEY:
    ai_client = genai.Client(api_key=config.GEMINI_API_KEY)


# ─────────────────────────────────────────────
# System prompt (inject channel mention động)
# ─────────────────────────────────────────────
def _build_system_prompt() -> str:
    announcements_mention = _announcements_mention()
    return f"""Bạn là Trợ lý AI của khóa học AI Thực Chiến, hỗ trợ cả học viên lẫn TA/Mod trên Discord.

GIỌNG ĐIỆU BẮT BUỘC:
- Xưng "mình", gọi người hỏi là "em" (với học viên) hoặc "bạn" (nếu nhận ra là TA/Mod qua ngữ cảnh).
- Thân thiện, nhẹ nhàng như nói chuyện với người quen — KHÔNG cứng nhắc, KHÔNG dùng từ máy móc như "Xin lưu ý", "Theo quy định số...".
- Câu trả lời tự nhiên, đủ ý nhưng gọn — KHÔNG liệt kê dài dòng nếu không cần thiết.
- Nếu không biết hoặc không có căn cứ: nói thẳng, nhẹ nhàng, KHÔNG đoán mò.

NHIỆM VỤ:
Phân loại intent và trả lời chính xác, an toàn dựa trên DỮ LIỆU CHÍNH THỨC bên dưới.

DANH SÁCH INTENT & QUY TẮC PHẢN HỒI:
1. GREETING — Chào hỏi / giao tiếp xã giao:
   - Chào lại thân thiện, giới thiệu ngắn mình có thể hỗ trợ gì (1-2 câu).
   - need_ta = false.

2. LOGISTICS_GROUNDED — Hỏi hạn nộp, quy cách, lịch, standup CÓ TRONG DỮ LIỆU CHÍNH THỨC:
   - Trả lời trực tiếp, TỐI ĐA 2-3 câu, giọng thân thiện.
   - need_ta = false.

3. LOGISTICS_UNGROUNDED — Hỏi thủ tục/deadline CHƯA CÓ THÔNG BÁO CHÍNH THỨC:
   - TUYỆT ĐỐI KHÔNG PHỎNG ĐOÁN DEADLINE — sai thông tin này ảnh hưởng điểm số của em.
   - Trả lời 1-2 câu: thành thật nói chưa có thông báo chính thức, hướng em theo dõi kênh {announcements_mention} để cập nhật mới nhất.
   - need_ta = true.

4. OUT_OF_SCOPE_PERSONAL — Yêu cầu tra điểm cá nhân, điểm danh cá nhân, xin châm chước nộp trễ:
   - Giải thích nhẹ nhàng mình không có thẩm quyền xử lý việc này (1-2 câu).
   - need_ta = true.

5. TECHNICAL_QUESTION — Hỏi kỹ thuật, code, git, cài đặt:
   - Gợi ý hướng xử lý ngắn gọn (1-2 câu), nếu phức tạp thì hướng dẫn em tạo ticket.
   - need_ta = false.

ĐỊNH DẠNG ĐẦU RA — trả về DUY NHẤT 1 chuỗi JSON hoàn chỉnh:
{{
  "intent": "GREETING | LOGISTICS_GROUNDED | LOGISTICS_UNGROUNDED | OUT_OF_SCOPE_PERSONAL | TECHNICAL_QUESTION",
  "need_ta": true/false,
  "confidence": <số thực 0.0–1.0 thể hiện độ tin cậy phân loại intent>,
  "thinking": {{
    "step1_intent": "<Nhận diện intent là gì, tại sao>",
    "step2_source_check": "<Đã tìm/kiểm tra nguồn nào trong KB, kết quả ra sao. Nếu không cần kiểm tra thì ghi N/A>",
    "step3_decision": "<Quyết định cuối: trả lời thẳng / escalate TA / từ chối, lý do>"
  }},
  "reply": "Nội dung trả lời — giọng thân thiện, xưng mình, gọi em, KHÔNG có đường dẫn file nội bộ."
}}
"""


SYSTEM_PROMPT = _build_system_prompt()

# ─────────────────────────────────────────────
# Màu & nhãn theo intent
# ─────────────────────────────────────────────
INTENT_COLORS = {
    "GREETING":              discord.Color.blurple(),
    "LOGISTICS_GROUNDED":    discord.Color.green(),
    "LOGISTICS_UNGROUNDED":  discord.Color.gold(),
    "OUT_OF_SCOPE_PERSONAL": discord.Color.red(),
    "TECHNICAL_QUESTION":    discord.Color.blue(),
    "UNKNOWN":               discord.Color.greyple(),
}

INTENT_LABELS = {
    "GREETING":              "💬 Chào hỏi / Giao tiếp",
    "LOGISTICS_GROUNDED":    "✅ Logistics — Có căn cứ nguồn",
    "LOGISTICS_UNGROUNDED":  "⚠️ Logistics — Chưa có thông báo chính thức",
    "OUT_OF_SCOPE_PERSONAL": "🔒 Ngoài thẩm quyền — Dữ liệu cá nhân",
    "TECHNICAL_QUESTION":    "🔧 Câu hỏi kỹ thuật",
    "UNKNOWN":               "❓ Không xác định",
}


# ─────────────────────────────────────────────
# Core AI call
# ─────────────────────────────────────────────
DEFAULT_FALLBACK = {
    "intent": "LOGISTICS_UNGROUNDED",
    "need_ta": True,
    "confidence": 0.0,
    "thinking": {
        "step1_intent": "Không thể kết nối AI để phân loại.",
        "step2_source_check": "N/A",
        "step3_decision": "Fallback: chuyển TA do không có kết quả từ AI.",
    },
    "reply": "Hiện tại chưa có thông tin chính thức cho câu hỏi này.",
}


def query_ai_assistant(user_question: str, case_id: str = "") -> dict:
    """
    Gọi Gemini để phân loại intent + sinh phản hồi có thinking steps.
    Mọi lời gọi đều được log vào eval/.
    """
    if not ai_client:
        logging.warning("Chưa cấu hình GEMINI_API_KEY!")
        return DEFAULT_FALLBACK

    # Lấy context KB — search theo câu hỏi để giảm token
    relevant = kb.search(user_question, top_k=8)
    context_str = kb.format_for_prompt(relevant if relevant else None)

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"DỮ LIỆU CHÍNH THỨC KHÓA HỌC:\n{context_str}\n\n"
        f"CÂU HỎI: {user_question}\n\n"
        f"KẾT QUẢ JSON:"
    )

    raw_text = ""
    parsed = DEFAULT_FALLBACK.copy()

    try:
        model_name = getattr(config, "GEMINI_MODEL", "gemini-3.5-flash-lite")
        response = ai_client.models.generate_content(model=model_name, contents=prompt)
        raw_text = response.text.strip()

        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            # Đảm bảo luôn có đủ key dù model quên trả
            if "thinking" not in parsed:
                parsed["thinking"] = {
                    "step1_intent": parsed.get("intent", "N/A"),
                    "step2_source_check": "Không có thông tin chi tiết từ AI.",
                    "step3_decision": "Quyết định dựa trên intent đã phân loại.",
                }
            if "confidence" not in parsed:
                parsed["confidence"] = 0.9
        else:
            logging.warning(f"Không parse được JSON: {raw_text[:200]}")

    except Exception as e:
        logging.error(f"Lỗi Gemini API: {e}")
        parsed = _keyword_fallback(user_question)

    finally:
        log_ai_call(case_id, user_question, prompt, raw_text, parsed)

    return parsed


def _keyword_fallback(question: str) -> dict:
    """Fallback cục bộ khi API lỗi/hết quota — dùng KB search."""
    results = kb.search(question, top_k=1)
    if results:
        item = results[0]
        return {
            "intent": "LOGISTICS_GROUNDED",
            "need_ta": False,
            "confidence": 0.5,
            "thinking": {
                "step1_intent": "Fallback keyword search do API lỗi.",
                "step2_source_check": f"Tìm thấy KB item: {item['id']} — {item['title']}",
                "step3_decision": "Trả lời từ KB cục bộ, không qua AI.",
            },
            "reply": f"{item['title']}: {item['content']}",
        }
    return DEFAULT_FALLBACK.copy()


# ─────────────────────────────────────────────
# Thinking UI — Embed + Button
# ─────────────────────────────────────────────
def build_thinking_embed(
    intent: str,
    confidence: float,
    thinking: dict,
    question: str,
) -> discord.Embed:
    """Tạo Embed hiển thị quy trình suy nghĩ của AI (chỉ người bấm nút mới thấy)."""
    color    = INTENT_COLORS.get(intent, discord.Color.greyple())
    label    = INTENT_LABELS.get(intent, intent)
    conf_pct = f"{confidence * 100:.1f}%"

    embed = discord.Embed(title="🤔 Quy trình suy nghĩ của AI", color=color)
    embed.set_footer(text="Track B1 · Trợ Lý Học Viên · Minh bạch quyết định AI")

    embed.add_field(
        name="📥 Câu hỏi nhận được",
        value=f"> {question[:200]}",
        inline=False,
    )
    embed.add_field(
        name="🤖 Bước 1 — Phân loại Intent",
        value=(
            f"**Intent:** `{intent}` — {label}\n"
            f"**Độ tin cậy:** `{conf_pct}`\n"
            f"_{thinking.get('step1_intent', 'N/A')}_"
        ),
        inline=False,
    )
    embed.add_field(
        name="🔍 Bước 2 — Kiểm tra căn cứ nguồn",
        value=f"_{thinking.get('step2_source_check', 'N/A')}_",
        inline=False,
    )
    embed.add_field(
        name="⚡ Bước 3 — Quyết định & Output",
        value=f"_{thinking.get('step3_decision', 'N/A')}_",
        inline=False,
    )
    return embed


class ThinkingView(View):
    """View chứa nút 'Thinking...' — bấm để xem quy trình AI (chỉ người bấm thấy)."""

    def __init__(self, intent: str, confidence: float, thinking: dict, question: str):
        super().__init__(timeout=300)  # Nút tồn tại 5 phút
        self.intent     = intent
        self.confidence = confidence
        self.thinking   = thinking
        self.question   = question

    @discord.ui.button(label="🤔 Thinking...", style=discord.ButtonStyle.secondary)
    async def show_thinking(self, interaction: discord.Interaction, button: Button):
        embed = build_thinking_embed(
            self.intent, self.confidence, self.thinking, self.question
        )
        # ephemeral=True: chỉ người bấm thấy, không spam kênh chung
        await interaction.response.send_message(embed=embed, ephemeral=True)


# ─────────────────────────────────────────────
# Discord commands (dành cho TA/Mod)
# ─────────────────────────────────────────────
@bot.event
async def on_ready():
    s = kb.stats()
    logging.info(f"✅ Bot online: {bot.user.name} (ID: {bot.user.id})")
    logging.info(f"📚 KB loaded: {s['total']} mục — {s['file']}")


@bot.command(name="add_kb")
async def cmd_add_knowledge(ctx, *, args: str):
    """
    TA/Mod thêm tri thức mới vào KB.
    Cú pháp: !add_kb Tiêu đề | Nội dung | Link (tùy chọn) | Category (tùy chọn)
    """
    parts = [p.strip() for p in args.split("|")]
    if len(parts) < 2:
        await ctx.send(
            "❌ Sai cú pháp!\n"
            "Dùng: `!add_kb Tiêu đề | Nội dung | Link (tùy chọn) | Category (tùy chọn)`"
        )
        return

    title    = parts[0]
    content  = parts[1]
    link     = parts[2] if len(parts) > 2 else ""
    category = parts[3] if len(parts) > 3 else "Cập nhật mới"

    item = kb.add_item(title=title, content=content, category=category, link=link)
    await ctx.send(
        f"✅ Đã thêm tri thức mới!\n"
        f"🆔 `{item['id']}` · 📂 {item['category']}\n"
        f"📌 **{title}**\n"
        f"📝 {content}"
    )


@bot.command(name="remove_kb")
async def cmd_remove_knowledge(ctx, item_id: str):
    """
    TA/Mod xóa mục KB theo ID.
    Cú pháp: !remove_kb QD_LAB_01
    """
    if kb.remove_item(item_id):
        await ctx.send(f"✅ Đã xóa mục `{item_id}` khỏi KB.")
    else:
        await ctx.send(f"❌ Không tìm thấy mục `{item_id}` trong KB.")


@bot.command(name="list_kb")
async def cmd_list_knowledge(ctx):
    """Liệt kê tất cả category và số mục trong KB."""
    s = kb.stats()
    if s["total"] == 0:
        await ctx.send("📋 KB hiện đang rỗng.")
        return
    lines = [f"📚 **KB hiện có {s['total']} mục:**"]
    for cat, count in sorted(s["categories"].items()):
        lines.append(f"  📂 {cat}: {count} mục")
    await ctx.send("\n".join(lines))


@bot.command(name="search_kb")
async def cmd_search_knowledge(ctx, *, query: str):
    """
    Tìm kiếm trong KB theo từ khóa.
    Cú pháp: !search_kb hạn nộp lab
    """
    results = kb.search(query, top_k=5)
    if not results:
        await ctx.send(f"🔍 Không tìm thấy kết quả cho: *{query}*")
        return
    lines = [f"🔍 Kết quả tìm kiếm **{query}** ({len(results)} mục):"]
    for item in results:
        lines.append(f"  • `{item['id']}` [{item['category']}] **{item['title']}**")
    await ctx.send("\n".join(lines))


# ─────────────────────────────────────────────
# Message handler
# ─────────────────────────────────────────────
@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Commands (!add_kb, !list_kb, ...) xử lý riêng
    await bot.process_commands(message)
    if message.content.startswith("!"):
        return

    # Kiểm tra bot được mention hoặc DM
    is_mentioned = bot.user.mentioned_in(message)
    is_role_mentioned = False
    if message.guild and message.guild.me:
        bot_roles = message.guild.me.roles
        is_role_mentioned = any(
            role in message.role_mentions
            for role in bot_roles
            if not role.is_default()
        )
    is_dm = isinstance(message.channel, discord.DMChannel)

    if not (is_mentioned or is_role_mentioned or is_dm):
        return

    # Làm sạch nội dung: xóa tất cả mentions
    content = re.sub(r'<@&?\!?\d+>', '', message.content).strip()
    if not content:
        await message.channel.send(
            "Chào em! 👋 Mình là Trợ lý Discord của khoá AI Thực Chiến. "
            "Em cần hỏi gì về hạn nộp bài, quy định hay kỹ thuật thì cứ nhắn mình nhé!"
        )
        return

    case_id = f"MSG_{message.id}"
    logging.info(f"📩 [{case_id}] #{message.channel} · {message.author}: {content[:80]}")

    async with message.channel.typing():
        result = query_ai_assistant(content, case_id=case_id)

        intent     = result.get("intent", "UNKNOWN")
        need_ta    = result.get("need_ta", False)
        confidence = result.get("confidence", 0.9)
        thinking   = result.get("thinking", {})
        reply      = result.get("reply", "")

        logging.info(
            f"   🎯 Intent: {intent} | Confidence: {confidence:.0%} | Need TA: {need_ta}"
        )

        ta_tag    = f"<@&{config.TA_ROLE_ID}>" if config.TA_ROLE_ID else "@TA"
        final_msg = (
            f"{reply}\n\n📣 {ta_tag} ơi, em cần được hỗ trợ thêm nha!"
            if need_ta else reply
        )

        # Gửi reply kèm nút Thinking (chỉ người bấm mới thấy embed)
        view = ThinkingView(intent, confidence, thinking, content)
        await message.channel.send(final_msg, view=view)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    if not config.DISCORD_TOKEN:
        print("❌ LỖI: Chưa cấu hình DISCORD_TOKEN trong file codebase/.env!")
    else:
        bot.run(config.DISCORD_TOKEN)
