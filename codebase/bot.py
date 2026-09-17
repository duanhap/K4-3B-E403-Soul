import os
import json
import re
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

# DỮ LIỆU THÔNG BÁO CHÍNH THỨC (Knowledge Base)
KNOWLEDGE_BASE = [
    {
        "id": "ANNOUNCEMENT_01",
        "title": "Hạn nộp Lab 01 & Quy cách commit GitHub",
        "content": "Hạn nộp Lab 01 là 21:00 ngày 18/9/2026. Học viên commit mã nguồn lên repo GitHub công khai cá nhân/nhóm và dán link commit vào kênh #submit-lab.",
        "link": "https://discord.com/channels/k4-3b/announcements/101"
    },
    {
        "id": "ANNOUNCEMENT_02",
        "title": "Quy định sự cố nộp muộn & Kỹ thuật",
        "content": "Mọi sự cố nộp muộn do Git/mạng cần báo trước hạn 15 phút kèm screenshot lỗi cho TA. Nộp muộn sau hạn không báo trước tính 0 điểm.",
        "link": "https://discord.com/channels/k4-3b/announcements/102"
    },
    {
        "id": "ANNOUNCEMENT_03",
        "title": "Lịch Checkpoint Hackathon (CP1 - CP4)",
        "content": "CP1: 19:30 17/9 (Canvas 7 dòng) | CP2: 21:00 17/9 (Luồng hoạt động) | CP3: 16:00 18/9 (Video 30s + số đo) | CP4: 21:00 18/9 (Chốt spec.md).",
        "link": "https://discord.com/channels/k4-3b/announcements/103"
    },
    {
        "id": "ANNOUNCEMENT_04",
        "title": "Quy định nộp Standup hàng ngày",
        "content": "Học viên gửi báo cáo Standup hàng ngày trước 09:00 sáng tại kênh #standup theo đúng template quy định.",
        "link": "https://discord.com/channels/k4-3b/announcements/104"
    },
    {
        "id": "STATUS_UNANNOUNCED",
        "title": "Các mục CHƯA CÓ THÔNG BÁO CHÍNH THỨC",
        "content": "Hạn nộp Lab 02, Lab 03, lịch thi Final, điểm danh cá nhân, kiểm tra điểm số cá nhân, yêu cầu xin châm chước commit trễ cá nhân -> Đều CHƯA có thông báo hoặc ngoài thẩm quyền tự động của bot.",
        "link": ""
    }
]

SYSTEM_PROMPT = """Bạn là Trợ lý AI Discord chuyên nghiệp cho khóa học (Track B1).

NHIỆM VỤ CỦA BẠN:
Phân loại intent câu hỏi của học viên và đưa ra phản hồi chính xác, an toàn.

DANH SÁCH INTENT & QUY TẮC PHẢN HỒI:
1. GREETING (Chào hỏi / Giao tiếp xã giao):
   - Phản hồi ngắn gọn, thân thiện (1 câu), nêu rõ bạn là Trợ lý hỗ trợ tra cứu thông tin logistics khóa học.
   - need_ta = false.

2. LOGISTICS_GROUNDED (Hỏi hạn nộp, quy cách, link, standup CÓ TRONG DỮ LIỆU CHÍNH THỨC):
   - Trả lời cực kỳ ngắn gọn: TỐI ĐA 2 CÂU.
   - BẮT BUỘC đính kèm link nguồn chính thức từ DỮ LIỆU CHÍNH THỨC.
   - need_ta = false.

3. LOGISTICS_UNGROUNDED (Hỏi thủ tục/deadline như "Lab 02", "Lab 03", "Thi final" nhưng CHƯA CÓ THÔNG BÁO CHÍNH THỨC):
   - NGUYÊN TẮC: TUYỆT ĐỐI KHÔNG PHỎNG ĐOÁN DEADLINE (Cost-of-Error rất đắt).
   - Phản hồi ngắn gọn (1 câu): Hiện tại chưa có thông báo chính thức về thông tin này.
   - need_ta = true.

4. OUT_OF_SCOPE_PERSONAL (Yêu cầu can thiệp dữ liệu cá nhân: tra điểm số, điểm danh cá nhân, xin châm chước nộp trễ):
   - Phản hồi ngắn gọn (1 câu): Bot không có thẩm quyền xử lý dữ liệu cá nhân hoặc duyệt châm chước.
   - need_ta = true.

5. TECHNICAL_QUESTION (Hỏi bài tập, thắc mắc kỹ thuật / code / git):
   - Gợi ý ngắn gọn hướng xử lý (1-2 câu).
   - need_ta = false (hoặc true nếu câu hỏi phức tạp cần TA can thiệp).

ĐỊNH DẠNG ĐẦU RA BẮT BUỘC (Trả về duy nhất 1 chuỗi JSON hoàn chỉnh):
{
  "intent": "GREETING | LOGISTICS_GROUNDED | LOGISTICS_UNGROUNDED | OUT_OF_SCOPE_PERSONAL | TECHNICAL_QUESTION",
  "need_ta": true/false,
  "reply": "Nội dung câu trả lời gửi tới học viên (Nếu là LOGISTICS_GROUNDED thì BẮT BUỘC có link nguồn)."
}
"""

def query_ai_assistant(user_question: str) -> dict:
    """Gọi Gemini API để phân loại Intent & sinh phản hồi có cấu trúc JSON."""
    default_fallback = {
        "intent": "LOGISTICS_UNGROUNDED",
        "need_ta": True,
        "reply": "Hiện tại chưa có thông tin chính thức cho câu hỏi này."
    }

    if not ai_client:
        print("   ⚠️ Chưa cấu hình GEMINI_API_KEY!")
        return default_fallback

    context_str = "\n".join([f"- [{kb['title']}] (Link: {kb['link']}): {kb['content']}" for kb in KNOWLEDGE_BASE])
    prompt = f"{SYSTEM_PROMPT}\n\nDỮ LIỆU CHÍNH THỨC KHÓA HỌC:\n{context_str}\n\nCÂU HỎI HỌC VIÊN: {user_question}\n\nKẾT QUẢ JSON:"

    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        raw_text = response.text.strip()
        
        # Trích xuất JSON từ phản hồi của AI (nếu có markdown block ```json)
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
    print("--- Đã tải Knowledge Base & Sẵn sàng phân loại intent ---")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
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
