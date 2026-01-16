import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")
