import os
import json
import re
from pathlib import Path
import discord
from discord.ext import commands
from google import genai
import config

# Khởi tạo Discord client với đầy đủ Intents
intents = discord.Intents.default()
intents.message_content = True  # Bắt buộc để đọc nội dung tin nhắn

bot = commands.Bot(command_prefix="!", intents=intents)

# Khởi tạo Gemini client nếu có API Key
ai_client = None
if config.GEMINI_API_KEY:
    ai_client = genai.Client(api_key=config.GEMINI_API_KEY)

# Đường dẫn file tri thức JSON
KB_FILE_PATH = Path(__file__).parent / "knowledge.json"

def load_knowledge_base() -> list:
    """Tải Knowledge Base từ file JSON."""
    if KB_FILE_PATH.exists():
        try:
            with open(KB_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Lỗi đọc file knowledge.json: {e}")
    return []

def save_knowledge_base(kb_data: list):
    """Lưu Knowledge Base vào file JSON."""
    try:
        with open(KB_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(kb_data, f, ensure_ascii=False, indent=2)
        print("✅ Đã lưu Knowledge Base vào file knowledge.json thành công.")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file knowledge.json: {e}")

# Tải Knowledge Base ban đầu
KNOWLEDGE_BASE = load_knowledge_base()

SYSTEM_PROMPT = """Bạn là Trợ lý AI Discord chuyên nghiệp cho khóa học (Track B1).

NHIỆM VỤ CỦA BẠN:
Phân loại intent câu hỏi của học viên và đưa ra phản hồi chính xác, an toàn dựa trên DỮ LIỆU CHÍNH THỨC.

DANH SÁCH INTENT & QUY TẮC PHẢN HỒI:
1. GREETING (Chào hỏi / Giao tiếp xã giao):
   - Phản hồi ngắn gọn, thân thiện (1 câu), nêu rõ bạn là Trợ lý hỗ trợ tra cứu thông tin logistics khóa học.
   - need_ta = false.

2. LOGISTICS_GROUNDED (Hỏi hạn nộp, quy cách, link, standup CÓ TRONG DỮ LIỆU CHÍNH THỨC):
   - Trả lời cực kỳ ngắn gọn: TỐI ĐA 2 CÂU.
   - BẮT BUỘC đính kèm link nguồn chính thức từ DỮ LIỆU CHÍNH THỨC.
   - need_ta = false.

3. LOGISTICS_UNGROUNDED (Hỏi thủ tục/deadline nhưng CHƯA CÓ THÔNG BÁO CHÍNH THỨC trong Dữ liệu):
   - NGUYÊN TẮC: TUYỆT ĐỐI KHÔNG PHỎNG ĐOÁN DEADLINE (Cost-of-Error rất đắt).
   - Phản hồi ngắn gọn (1 câu): Hiện tại chưa có thông báo chính thức về thông tin này.
   - need_ta = true.

4. OUT_OF_SCOPE_PERSONAL (Yêu cầu can thiệp dữ liệu cá nhân: tra điểm số, điểm danh cá nhân, xin châm chước nộp trễ):
   - Phản hồi ngắn gọn (1 câu): Bot không có thẩm quyền xử lý dữ liệu cá nhân hoặc duyệt châm chước.
   - need_ta = true.

5. TECHNICAL_QUESTION (Hỏi bài tập, thắc mắc kỹ thuật / code / git):
   - Gợi ý ngắn gọn hướng xử lý (1-2 câu).
   - need_ta = false.

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (Trả về duy nhất 1 chuỗi JSON hoàn chỉnh):
{
  "intent": "GREETING | LOGISTICS_GROUNDED | LOGISTICS_UNGROUNDED | OUT_OF_SCOPE_PERSONAL | TECHNICAL_QUESTION",
  "need_ta": true/false,
  "reply": "Nội dung câu trả lời gửi tới học viên (Nếu là LOGISTICS_GROUNDED thì BẮT BUỘC có link nguồn)."
}
"""

def query_ai_assistant(user_question: str) -> dict:
    """Gọi Gemini API để phân loại Intent & sinh phản hồi dựa trên Knowledge Base động."""
    default_fallback = {
        "intent": "LOGISTICS_UNGROUNDED",
        "need_ta": True,
        "reply": "Hiện tại chưa có thông tin chính thức cho câu hỏi này."
    }

    if not ai_client:
        print("   ⚠️ Chưa cấu hình GEMINI_API_KEY!")
        return default_fallback

    # Nạp dữ liệu Knowledge Base mới nhất
    current_kb = load_knowledge_base()
    context_str = "\n".join([f"- [{kb.get('title', '')}] (Link: {kb.get('link', '')}): {kb.get('content', '')}" for kb in current_kb])
    prompt = f"{SYSTEM_PROMPT}\n\nDỮ LIỆU CHÍNH THỨC KHÓA HỌC:\n{context_str}\n\nCÂU HỎI HỌC VIÊN: {user_question}\n\nKẾT QUẢ JSON:"

    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        raw_text = response.text.strip()
        
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(0))
            return parsed
        else:
            return default_fallback
    except Exception as e:
        print(f"   ❌ Lỗi khi gọi Gemini API: {e}")
        return default_fallback

@bot.event
async def on_ready():
    print(f"✅ Bot Trợ Lý Discord đã hoạt động: {bot.user.name} (ID: {bot.user.id})")
    print(f"--- Đã tải {len(load_knowledge_base())} mục tri thức từ knowledge.json ---")

@bot.command(name="add_kb")
async def add_knowledge(ctx, *, args: str):
    """Lệnh dành cho TA/Mod cập nhật tri thức mới trực tiếp từ Discord.
    Cú pháp: !add_kb Tiêu đề thông báo | Nội dung chi tiết | Link nguồn
    """
    parts = [p.strip() for p in args.split("|")]
    if len(parts) < 2:
        await ctx.send("❌ Sai cú pháp! Dùng: `!add_kb Tiêu đề | Nội dung chi tiết | Link nguồn (tùy chọn)`")
        return

    title = parts[0]
    content = parts[1]
    link = parts[2] if len(parts) > 2 else ""

    kb_list = load_knowledge_base()
    new_item = {
        "id": f"KB_{len(kb_list) + 1:02d}",
        "category": "Cập nhật mới",
        "title": title,
        "content": content,
        "link": link
    }
    kb_list.append(new_item)
    save_knowledge_base(kb_list)

    await ctx.send(f"✅ Đã thêm tri thức mới thành công!\n📌 **{title}**\n📝 {content}\n🔗 {link or 'Không có link'}")

@bot.command(name="list_kb")
async def list_knowledge(ctx):
    """Liệt kê tất cả danh mục tri thức hiện có trong Knowledge Base."""
    kb_list = load_knowledge_base()
    if not kb_list:
        await ctx.send("📋 Tri thức hiện tại đang rỗng.")
        return

    msg = f"📋 **DANH SÁCH TRI THỨC HIỆN CÓ ({len(kb_list)} mục):**\n"
    for item in kb_list[:10]:  # Giới hạn 10 mục
        msg += f"• **{item.get('title')}**: {item.get('content')[:60]}...\n"
    await ctx.send(msg)

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # Nếu là lệnh !add_kb hoặc !list_kb thì để bot xử lý command
    if message.content.startswith("!add_kb") or message.content.startswith("!list_kb"):
        await bot.process_commands(message)
        return

    # Kiểm tra xem Bot được tag trực tiếp (User Mention) hay tag qua Role của Bot (Role Mention)
    is_user_mentioned = bot.user.mentioned_in(message)
    is_role_mentioned = False
    if message.guild and message.guild.me:
        bot_roles = message.guild.me.roles
        is_role_mentioned = any(role in message.role_mentions for role in bot_roles if not role.is_default())

    is_mentioned = is_user_mentioned or is_role_mentioned
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_command = message.content.startswith("!")

    if is_mentioned or is_dm or is_command:
        print(f"📩 [Tin nhắn mới] Kênh: #{message.channel} | Từ: {message.author} | Tag Bot/Role: {is_mentioned}")
        print(f"   Nội dung gốc: '{message.content}'")

        # Làm sạch nội dung câu hỏi: Xóa tất cả tag <@ID>, <@!ID>, <@&ID>
        content = re.sub(r'<@&?\!?\d+>', '', message.content).strip()
        if content.startswith("!"):
            content = content[1:].strip()

        if not content:
            await message.channel.send("Chào bạn! Mình là Trợ lý Discord. Bạn cần hỗ trợ thông tin gì về hạn nộp bài hay quy định khóa học?")
            return

        async with message.channel.typing():
            print(f"   🔍 Đang phân loại Intent cho câu hỏi: '{content}'...")
            ai_res = query_ai_assistant(content)
            
            intent = ai_res.get("intent", "UNKNOWN")
            need_ta = ai_res.get("need_ta", False)
            reply_text = ai_res.get("reply", "")

            print(f"   🎯 Intent nhận diện: {intent} | Need TA: {need_ta}")
            print(f"   💬 Phản hồi: '{reply_text}'")

            ta_tag = f"<@&{config.TA_ROLE_ID}>" if config.TA_ROLE_ID else "@TA"

            if need_ta:
                final_msg = f"{reply_text}\n⚠️ {ta_tag} hỗ trợ học viên giúp mình nhé!"
            else:
                final_msg = reply_text

            await message.channel.send(final_msg)

    await bot.process_commands(message)

if __name__ == "__main__":
    if not config.DISCORD_TOKEN:
        print("❌ LỖI: Chưa cấu hình DISCORD_TOKEN trong file codebase/.env!")
    else:
        bot.run(config.DISCORD_TOKEN)
