import os
from pathlib import Path
from dotenv import load_dotenv

# Tìm và load file .env nằm cùng thư mục với config.py
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TA_ROLE_ID = os.getenv("TA_ROLE_ID", "").strip()
ANNOUNCEMENTS_CHANNEL_ID = os.getenv("ANNOUNCEMENTS_CHANNEL_ID", "").strip()
