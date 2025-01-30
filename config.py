# config.py
from dotenv import load_dotenv
import os
import pytz

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HISTORY_DIR = "history"
    VN_TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')

class MessageLimits:
    INITIAL_LIMIT = 10
    EXTENDED_LIMIT = 20
    FINAL_LIMIT = 35
    COOLDOWN = 3
    VALID_KEY = "Behoane"