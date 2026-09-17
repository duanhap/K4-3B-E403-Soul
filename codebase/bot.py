import os
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

SYSTEM_PROMPT = """Bạn là Trợ lý Discord cho học viên khóa học (Track B1).
Nhiệm vụ của bạn:
1. Giải đáp các thắc mắc về LOGISTICS (hạn nộp bài, hình thức nộp, link nộp bài, quy định điểm danh, sự cố nộp muộn) dựa trên dữ liệu chính thức.
2. NGUYÊN TẮC BẮT BUỘC:
   - Trả lời cực kỳ ngắn gọn: TỐI ĐA 2 CÂU.
   - Luôn kèm theo link hoặc nguồn thông báo chính thức nếu có.
   - KHÔNG phỏng đoán deadline hoặc quy định khi chưa có thông báo chính thức.
   - KHÔNG can thiệp/trả lời các thông tin dữ liệu cá nhân (điểm số cá nhân, điểm danh cá nhân).
   - Nếu KHÔNG CÓ CĂN CỨ hoặc VƯỢT THẨM QUYỀN, hãy trả lời chính xác: "HIEN_THUYET_CHUA_CO_THONG_TIN" để hệ thống tự động tag TA hỗ trợ.
"""

# Dữ liệu mẫu thông báo chính thức (Logistics Knowledge Base)
KNOWLEDGE_BASE = [
    {
        "title": "Hạn nộp Lab 01 & Quy cách commit",
        "content": "Hạn nộp Lab 01 là 21:00 ngày 18/9/2026. Học viên commit mã nguồn lên repo GitHub cá nhân/nhóm và dán link commit vào kênh #submit-lab.",
        "link": "https://discord.com/channels/example/announcements/101"
    },
    {
        "title": "Quy định nộp muộn & Sự cố kỹ thuật",
        "content": "Mọi sự cố nộp muộn do Git/mạng cần báo trước hạn 15 phút kèm screenshot lỗi cho TA. Nộp muộn sau hạn không báo trước tính 0 điểm.",
        "link": "https://discord.com/channels/example/announcements/102"
    }
]

def query_ai_assistant(user_question: str) -> str:
    if not ai_client:
        return "HIEN_THUYET_CHUA_CO_THONG_TIN"

    context_str = "\n".join([f"- [{kb['title']}] ({kb['link']}): {kb['content']}" for kb in KNOWLEDGE_BASE])
    prompt = f"{SYSTEM_PROMPT}\n\nDỮ LIỆU CHÍNH THỨC:\n{context_str}\n\nCÂU HỎI HỌC VIÊN: {user_question}\nTRẢ LỜI:"
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',  # Tên model chuẩn của Google
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Lỗi AI API: {e}")
        return "HIEN_THUYET_CHUA_CO_THONG_TIN"

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập thành công với tên: {bot.user.name} (ID: {bot.user.id})")
    print("--- sẵn sàng nhận câu hỏi ---")

@bot.event
async def on_message(message: discord.Message):
    # Tránh bot tự trả lời tin nhắn của chính mình
    if message.author == bot.user:
        return

    # In log nhận tin nhắn để người dùng dễ kiểm tra trên Terminal
    is_mentioned = bot.user.mentioned_in(message)
    print(f"📩 [Tin nhắn mới] Kênh: #{message.channel} | Tác giả: {message.author} | Tag Bot: {is_mentioned}")
    print(f"   Nội dung thô: '{message.content}'")

    # Nếu tin nhắn tag bot / nhắn trực tiếp DM / câu hỏi bắt đầu bằng !
    if is_mentioned or isinstance(message.channel, discord.DMChannel) or message.content.startswith("!"):
        # Xóa tag bot (xử lý cả <@ID> và <@!ID>)
        content = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()
        if content.startswith("!"):
            content = content[1:].strip()

        print(f"   🔍 Nội dung câu hỏi sau xử lý: '{content}'")

        if not content:
            print("   ⚠️ Câu hỏi rỗng, gửi lời chào...")
            await message.channel.send("Chào bạn, mình có thể giúp gì về thông tin hạn nộp bài và thủ tục khóa học?")
            return

        async with message.channel.typing():
            print("   🤖 Đang gọi AI xử lý câu hỏi...")
            answer = query_ai_assistant(content)
            print(f"   💡 AI phản hồi: '{answer}'")

            ta_tag = f"<@&{config.TA_ROLE_ID}>" if config.TA_ROLE_ID else "@TA"

            if "HIEN_THUYET_CHUA_CO_THONG_TIN" in answer or not answer:
                await message.channel.send(
                    f"⚠️ Hiện tại chưa có thông tin chính thức cho câu hỏi này. {ta_tag} hỗ trợ bạn nhé!"
                )
            else:
                await message.channel.send(answer)

    await bot.process_commands(message)

if __name__ == "__main__":
    if not config.DISCORD_TOKEN:
        print("❌ LỖI: Chưa cấu hình DISCORD_TOKEN trong file .env!")
        print("Hãy copy file codebase/.env.example thành codebase/.env và điền Token của bot.")
    else:
        bot.run(config.DISCORD_TOKEN)
