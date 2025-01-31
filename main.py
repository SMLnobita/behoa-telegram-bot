# main.py
import os
import telebot
from config import Config
from handlers.message_commands import MessageCommands
from handlers.callback_handler import CallbackHandler
from handlers.chat_handler import ChatHandler
from managers.user_manager import UserManager
from utils.openai_handler import OpenAIHandler
from trackers.currency_tracker import CurrencyExchangeTracker
from trackers.gold_tracker import GoldPriceTracker
from trackers.crypto_tracker import CryptoPriceTracker
from utils.message_handler import MessageHandler

class TelegramBot:
    def __init__(self):
        """Initialize the Telegram bot and all its components"""
        # Initialize the bot
        self.bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)
        
        # Initialize managers
        self.user_manager = UserManager()
        
        # Initialize handlers and trackers
        self.openai_handler = OpenAIHandler()
        self.gold_tracker = GoldPriceTracker()
        self.currency_tracker = CurrencyExchangeTracker()
        self.crypto_tracker = CryptoPriceTracker()

        # Create trackers dictionary for dependency injection
        trackers = {
            'gold': self.gold_tracker,
            'currency': self.currency_tracker,
            'crypto': self.crypto_tracker,
            'openai': self.openai_handler
        }

        # Initialize command handlers
        self.message_commands = MessageCommands(self.bot, self.user_manager, trackers)
        self.callback_handler = CallbackHandler(self.bot, self.user_manager)
        self.chat_handler = ChatHandler(self.bot, self.user_manager, trackers)

        # Set up bot commands
        self._setup_commands()
        
        # Register all handlers
        self._register_handlers()

    def _setup_commands(self):
        """Thiết lập danh sách lệnh cho bot"""
        self.bot.set_my_commands([
            telebot.types.BotCommand("start", "Khởi động bot"),
            telebot.types.BotCommand("help", "Xem hướng dẫn sử dụng"),
            telebot.types.BotCommand("clear", "Xóa lịch sử chat"),
            telebot.types.BotCommand("time", "Xem thời gian hiện tại"),
            telebot.types.BotCommand("info", "Xem thông tin của bạn"),
            telebot.types.BotCommand("image", "Tạo hình ảnh từ mô tả"),
            telebot.types.BotCommand("vang", "Xem giá vàng SJC và PNJ"),
            telebot.types.BotCommand("ngoaite", "Xem tỷ giá ngoại tệ"),
            telebot.types.BotCommand("tienao", "Xem giá tiền ảo")
        ])

    def _register_handlers(self):
        """Đăng ký tất cả các handlers cho bot"""
        # Command handlers
        self.bot.message_handler(commands=['start'])(self.message_commands.start_message)
        self.bot.message_handler(commands=['help'])(self.message_commands.help_message)
        self.bot.message_handler(commands=['clear'])(self.message_commands.clear_message)
        self.bot.message_handler(commands=['info'])(self.message_commands.info_message)
        self.bot.message_handler(commands=['image'])(self.message_commands.image_message)
        self.bot.message_handler(commands=['time'])(self.message_commands.time_message)
        self.bot.message_handler(commands=['vang'])(self.message_commands.gold_price_message)
        self.bot.message_handler(commands=['ngoaite'])(self.message_commands.exchange_rate_message)
        self.bot.message_handler(commands=['tienao'])(self.message_commands.crypto_price_message)

        # Callback handler for inline buttons
        self.bot.callback_query_handler(func=lambda call: True)(
            self.callback_handler.handle_callback
        )

        # General message handler for chat and keywords
        self.bot.message_handler(func=lambda message: True)(
            self.chat_handler.handle_message
        )

    def run(self):
        """Khởi chạy bot"""
        print("🚀 Chatbot GPT-4o trên Telegram đang chạy...")
        print(f"⏰ Khởi động lúc: {MessageHandler.format_time_message()}")
        try:
            self.bot.polling(none_stop=True)
        except Exception as e:
            print(f"❌ Lỗi khi chạy bot: {str(e)}")
            # Có thể thêm logic retry hoặc xử lý lỗi ở đây

def main():
    """Entry point của ứng dụng"""
    try:
        # Ensure config is valid
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram Bot Token không được để trống")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key không được để trống")

        # Create and run the bot
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Lỗi khởi tạo bot: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()