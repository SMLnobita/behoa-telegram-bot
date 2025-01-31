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
from trackers.weather_tracker import WeatherAirQualityTracker
from utils.message_handler import MessageHandler

class TelegramBot:
    def __init__(self):
        """Khởi tạo bot Telegram và tất cả các thành phần của nó"""
        # Khởi tạo bot
        self.bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)
        
        # Khởi tạo các manager
        self.user_manager = UserManager()
        
        # Khởi tạo các handler và tracker
        self.openai_handler = OpenAIHandler()
        self.gold_tracker = GoldPriceTracker()
        self.currency_tracker = CurrencyExchangeTracker()
        self.crypto_tracker = CryptoPriceTracker()
        self.weather_tracker = WeatherAirQualityTracker()

        # Tạo dictionary trackers để tiêm phụ thuộc
        trackers = {
            'gold': self.gold_tracker,
            'currency': self.currency_tracker,
            'crypto': self.crypto_tracker,
            'openai': self.openai_handler,
            'weather': self.weather_tracker 
        }

        # Khởi tạo các command handler
        self.message_commands = MessageCommands(self.bot, self.user_manager, trackers)
        self.callback_handler = CallbackHandler(self.bot, self.user_manager)
        self.chat_handler = ChatHandler(self.bot, self.user_manager, trackers)

        # Thiết lập các lệnh cho bot
        self._setup_commands()
        
        # Đăng ký tất cả các handler
        self._register_handlers()

    def _setup_commands(self):
        """Thiết lập danh sách lệnh cho bot"""
        self.bot.set_my_commands([
            telebot.types.BotCommand("start", "Khởi động bot"),
            telebot.types.BotCommand("help", "Xem hướng dẫn sử dụng"),
            telebot.types.BotCommand("clear", "Xóa lịch sử chat"),
            telebot.types.BotCommand("time", "Xem thời gian hiện tại"),
            telebot.types.BotCommand("thoitiet", "Xem thời tiết và chất lượng không khí"),
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
        self.bot.message_handler(commands=['thoitiet'])(self.message_commands.weather_message)
        self.bot.message_handler(commands=['vang'])(self.message_commands.gold_price_message)
        self.bot.message_handler(commands=['ngoaite'])(self.message_commands.exchange_rate_message)
        self.bot.message_handler(commands=['tienao'])(self.message_commands.crypto_price_message)

        # Callback handler cho inline buttons
        self.bot.callback_query_handler(func=lambda call: True)(
            self.callback_handler.handle_callback
        )

        # General message handler cho chat và từ khóa
        self.bot.message_handler(func=lambda message: True)(
            self.chat_handler.handle_message
        )

    def run(self):
        """Khởi chạy bot"""
        print("🚀 Chatbot GPT-4o-mini trên Telegram đang chạy...")
        print(f"⏰ Khởi động lúc: {MessageHandler.format_time_message()}")
        try:
            self.bot.polling(none_stop=True)
        except Exception as e:
            print(f"❌ Lỗi khi chạy bot: {str(e)}")
            # Có thể thêm logic retry hoặc xử lý lỗi ở đây

def main():
    """Điểm vào của ứng dụng"""
    try:
        # Đảm bảo config hợp lệ
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("Telegram Bot Token không được để trống")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key không được để trống")

        # Tạo và chạy bot
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        print(f"❌ Lỗi khởi tạo bot: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()