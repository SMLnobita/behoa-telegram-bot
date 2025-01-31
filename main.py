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
from trackers.weather_tracker import WeatherTracker

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
        self.weather_tracker = WeatherTracker()

        # Create trackers dictionary for dependency injection
        trackers = {
            'gold': self.gold_tracker,
            'currency': self.currency_tracker,
            'crypto': self.crypto_tracker,
            'weather': self.weather_tracker,
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
        """Set up the list of commands for the bot"""
        self.bot.set_my_commands([
            telebot.types.BotCommand("start", "Bắt đầu trò chuyện với bot"),
            telebot.types.BotCommand("help", "Xem danh sách các lệnh"),
            telebot.types.BotCommand("clear", "Xóa tin nhắn của bot"),
            telebot.types.BotCommand("info", "Xem thông tin của bạn"),
            telebot.types.BotCommand("thoitiet", "Xem thời tiết hiện tại"),
            telebot.types.BotCommand("image", "Tạo hình ảnh từ mô tả"),
            telebot.types.BotCommand("time", "Xem giờ hiện tại"),
            telebot.types.BotCommand("vang", "Xem giá vàng (SJC và PNJ)"),
            telebot.types.BotCommand("ngoaite", "Xem tỷ giá ngoại tệ"),
            telebot.types.BotCommand("tienao", "Xem giá tiền điện tử"),
        ])

    def _register_handlers(self):
        """Register all handlers for the bot"""
        # Command handlers
        self.bot.message_handler(commands=['start'])(self.message_commands.start_message)
        self.bot.message_handler(commands=['help'])(self.message_commands.help_message)
        self.bot.message_handler(commands=['clear'])(self.message_commands.clear_message)
        self.bot.message_handler(commands=['info'])(self.message_commands.info_message)
        self.bot.message_handler(commands=['thoitiet'])(self.message_commands.weather_message)
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
        """Run the bot"""
        print("🚀 Chatbot GPT-4o on Telegram is running...")
        print(f"⏰ Started at: {MessageHandler.format_time_message()}")
        try:
            self.bot.polling(none_stop=True)
        except Exception as e:
            print(f"❌ Error running bot: {str(e)}")
            # Add retry logic or error handling here if needed

def main():
    """Entry point of the application"""
    try:
        # Ensure config is valid
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram Bot Token cannot be empty")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key cannot be empty")

        # Create and run the bot
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Error initializing bot: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()