import telebot
import os
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

from config import Config, MessageLimits
from models import UserState
from enums import UserStage
from trackers.currency_tracker import CurrencyExchangeTracker
from trackers.gold_tracker import GoldPriceTracker
from trackers.crypto_tracker import CryptoPriceTracker
from utils.message_handler import MessageHandler
from utils.openai_handler import OpenAIHandler

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)
        self.openai_handler = OpenAIHandler()
        self.gold_tracker = GoldPriceTracker()
        self.currency_tracker = CurrencyExchangeTracker()
        self.crypto_tracker = CryptoPriceTracker()
        self.users = {}

        if not os.path.exists(Config.HISTORY_DIR):
            os.makedirs(Config.HISTORY_DIR)

        self._register_handlers()

    def _can_send_message(self, user_state):
        """Kiểm tra xem người dùng có thể gửi tin nhắn không"""
        current_time = time.time()
        if current_time - user_state.last_message_time < MessageLimits.COOLDOWN:
            return False
        return True

    def _check_message_limit(self, user_state):
        """Kiểm tra giới hạn tin nhắn dựa trên trạng thái"""
        count = user_state.message_count
        stage = user_state.stage

        if stage == UserStage.INITIAL and count >= MessageLimits.INITIAL_LIMIT:
            return False
        elif stage == UserStage.EXTENDED and count >= MessageLimits.EXTENDED_LIMIT:
            return False
        elif stage == UserStage.KEY_USED and count >= MessageLimits.FINAL_LIMIT:
            return False
        return True

    def _clear_user_data(self, user_id):
        """Xóa toàn bộ dữ liệu của người dùng"""
        MessageHandler.clear_chat_history(user_id)
        self.users[user_id] = UserState()

    def _get_user_state(self, user_id):
        """Lấy hoặc tạo mới trạng thái người dùng"""
        if user_id not in self.users:
            self.users[user_id] = UserState()
        return self.users[user_id]

    def _register_handlers(self):
        """Đăng ký tất cả các handlers cho bot"""
        self.bot.message_handler(commands=['start'])(self.start_message)
        self.bot.message_handler(commands=['help'])(self.help_message)
        self.bot.message_handler(commands=['info'])(self.info_message)
        self.bot.message_handler(commands=['clear'])(self.clear_message)
        self.bot.message_handler(commands=['time'])(self.time_message)
        self.bot.message_handler(commands=['vang'])(self.gold_price_message)
        self.bot.message_handler(commands=['ngoaite'])(self.exchange_rate_message)
        self.bot.message_handler(commands=['tienao'])(self.crypto_price_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_handler)
        self.bot.message_handler(func=lambda message: True)(self.handle_message)

    def callback_handler(self, call):
        """Xử lý callback từ các nút"""
        user_id = call.message.chat.id
        user_state = self._get_user_state(user_id)

        if call.data == "start":
            self.bot.send_message(user_id, "💬 Hãy bắt đầu chat!")
            
        elif call.data == "clear":
            self._clear_user_data(user_id)
            self.bot.send_message(
                user_id,
                "🧹 **Lịch sử chat đã được xóa!** Bạn có thể tiếp tục chat mới.",
                parse_mode="Markdown"
            )
            
        elif call.data == "continue" and user_state.stage == UserStage.INITIAL:
            user_state.stage = UserStage.EXTENDED
            remaining = MessageLimits.EXTENDED_LIMIT - user_state.message_count
            self.bot.send_message(
                user_id, 
                f"✨ Bạn đã được cấp thêm {remaining} tin nhắn!"
            )
            
        elif call.data == "request_key" and user_state.stage == UserStage.EXTENDED:
            user_state.waiting_for_key = True
            self.bot.send_message(
                user_id,
                "🔑 Vui lòng nhập key để được cấp thêm tin nhắn:",
                reply_markup=ForceReply()
            )

    def clear_message(self, message):
        """Xử lý lệnh /clear"""
        user_id = message.chat.id
        self._clear_user_data(user_id)
        self.bot.send_message(
            user_id,
            "🧹 **Lịch sử chat đã được xóa!** Bạn có thể tiếp tục chat mới.",
            parse_mode="Markdown"
        )

    def crypto_price_message(self, message):
        """Xử lý lệnh /tienao"""
        try:
            crypto_data = self.crypto_tracker.fetch_crypto_prices()
            formatted_message = self.crypto_tracker.format_crypto_prices(crypto_data)
            self.bot.send_message(
                message.chat.id,
                formatted_message,
                parse_mode="Markdown"
            )
        except Exception as e:
            error_message = f"❌ {str(e)}"
            self.bot.send_message(
                message.chat.id,
                error_message,
                parse_mode="Markdown"
            )

    def exchange_rate_message(self, message):
        """Xử lý lệnh /ngoaite"""
        try:
            rates = self.currency_tracker.fetch_exchange_rates()
            formatted_message = self.currency_tracker.format_exchange_rates(rates)
            self.bot.send_message(
                message.chat.id,
                formatted_message,
                parse_mode="Markdown"
            )
        except Exception as e:
            error_message = f"❌ {str(e)}"
            self.bot.send_message(
                message.chat.id,
                error_message,
                parse_mode="Markdown"
            )

    def gold_price_message(self, message):
        """Xử lý lệnh /vang"""
        try:
            gold_data = self.gold_tracker.fetch_gold_prices()
            formatted_message = self.gold_tracker.format_gold_prices(gold_data)
            self.bot.send_message(
                message.chat.id,
                formatted_message,
                parse_mode="Markdown"
            )
        except Exception as e:
            error_message = f"❌ {str(e)}"
            self.bot.send_message(
                message.chat.id,
                error_message,
                parse_mode="Markdown"
            )

    def handle_message(self, message):
        """Xử lý tin nhắn từ người dùng"""
        user_id = message.chat.id
        user_state = self._get_user_state(user_id)

        if user_state.waiting_for_key:
            if message.text == MessageLimits.VALID_KEY:
                user_state.stage = UserStage.KEY_USED
                user_state.waiting_for_key = False
                remaining = MessageLimits.FINAL_LIMIT - user_state.message_count
                self.bot.send_message(
                    user_id, 
                    f"✅ Key hợp lệ! Bạn đã được cấp thêm {remaining} tin nhắn."
                )
                return
            else:
                user_state.waiting_for_key = False
                self.bot.send_message(user_id, "❌ Key không hợp lệ! Vui lòng thử lại sau.")
                return

        if not self._can_send_message(user_state):
            self.bot.send_message(
                user_id,
                "⏳ **Đợi một chút rồi hỏi tiếp nhé!**",
                parse_mode="Markdown"
            )
            return

        if not self._check_message_limit(user_state):
            menu = MessageHandler.create_menu_markup(user_state)
            message_text = "⚠️ **Bạn đã đạt giới hạn tin nhắn cho giai đoạn này!**"
            
            if user_state.stage == UserStage.INITIAL:
                message_text += "\nNhấn 'Tiếp tục nhắn' để được cấp thêm tin nhắn."
            elif user_state.stage == UserStage.EXTENDED:
                message_text += "\nNhập key để được cấp thêm tin nhắn."
            
            self.bot.send_message(
                user_id,
                message_text,
                parse_mode="Markdown",
                reply_markup=menu
            )
            return

        user_state.last_message_time = time.time()
        user_state.message_count += 1

        chat_history = MessageHandler.get_chat_history(user_id)
        messages = [{"role": "system", "content": "Bạn là một chatbot AI sử dụng GPT-4o."}]

        for chat in chat_history:
            if ": " in chat:
                try:
                    role, content = chat.split(": ", 1)
                    if role in ["user", "assistant", "system"]:
                        messages.append({"role": role, "content": content})
                except ValueError:
                    continue

        messages.append({"role": "user", "content": message.text})
        MessageHandler.add_to_chat_history(user_id, "user", message.text)

        time_info = MessageHandler.format_time_message()
        reply = self.openai_handler.process_message(messages, time_info)
        MessageHandler.add_to_chat_history(user_id, "assistant", reply)

        remaining = MessageHandler.get_remaining_messages(user_state)
        remaining_msg = f"\n\n💬 Bạn còn {remaining} tin nhắn."
        
        menu = MessageHandler.create_menu_markup(user_state)
        full_reply = f"{reply}{remaining_msg}"
        
        if menu:
            self.bot.send_message(
                user_id, 
                full_reply, 
                parse_mode="Markdown",
                reply_markup=menu
            )
        else:
            self.bot.send_message(
                user_id, 
                full_reply, 
                parse_mode="Markdown"
            )

    def help_message(self, message):
        """Xử lý lệnh /help"""
        help_text = (
            "🤖 **Hướng dẫn sử dụng BéHoà-4o Bot**\n\n"
            "**📝 Các lệnh cơ bản:**\n"
            "• `/start` - Khởi động bot và xóa lịch sử chat\n"
            "• `/help` - Hiển thị hướng dẫn sử dụng\n"
            "• `/clear` - Xóa lịch sử chat hiện tại\n"
            "• `/time` - Xem thời gian hiện tại\n"
            "• `/info` - Xem thông tin của bạn\n\n"
            "**💹 Tra cứu giá:**\n"
            "• `/vang` - Xem giá vàng SJC và PNJ\n"
            "• `/ngoaite` - Xem tỷ giá ngoại tệ Vietcombank\n"
            "• `/tienao` - Xem giá tiền ảo trên Binance\n\n"
            "**💬 Giới hạn chat:**\n"
            f"• Giai đoạn 1: {MessageLimits.INITIAL_LIMIT} tin nhắn\n"
            f"• Giai đoạn 2: {MessageLimits.EXTENDED_LIMIT} tin nhắn (sau khi nhấn 'Tiếp tục nhắn')\n"
            f"• Giai đoạn 3: {MessageLimits.FINAL_LIMIT} tin nhắn (sau khi nhập key)\n"
            f"• Thời gian chờ giữa các tin nhắn: {MessageLimits.COOLDOWN} giây\n\n"
            "**🔍 Lưu ý:**\n"
            "• liên hệ: @smlnobita (Telegram)\n"
            "• Bot có thể hiểu và trả lời bằng nhiều ngôn ngữ\n"
            "• Lịch sử chat sẽ được lưu cho đến khi bạn xóa hoặc khởi động lại\n"
            "• Có thể sử dụng nút menu để thực hiện các thao tác nhanh"
        )
        
        self.bot.send_message(
            message.chat.id,
            help_text,
            parse_mode="Markdown"
        )

    def info_message(self, message):
        """Xử lý lệnh /info"""
        try:
            user = message.from_user
            info = (
                "✨ **THÔNG TIN NGƯỜI DÙNG** ✨\n\n"
                f"🆔 **ID:** `{user.id}`\n"
                f"👤 **Username:** @{user.username if user.username else 'Không có'}\n"
                f"📛 **Tên:** {user.first_name} {user.last_name if user.last_name else ''}\n"
                f"🌐 **Ngôn ngữ:** {user.language_code if user.language_code else 'Không xác định'}\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📌 Hãy lưu lại thông tin này nếu cần thiết!"
            )

            self.bot.send_message(
                message.chat.id,
                info,
                parse_mode="Markdown"
            )
        except Exception as e:
            error_message = (
                "🚨 **LỖI!** 🚨\n"
                f"❌ Không thể lấy thông tin do lỗi sau:\n"
                f"`{str(e)}`\n\n"
                "⚙️ Vui lòng thử lại sau!"
            )
            self.bot.send_message(
                message.chat.id,
                error_message,
                parse_mode="Markdown"
            )

    def run(self):
        """Khởi chạy bot"""
        print("🚀 Chatbot GPT-4o trên Telegram đang chạy...")
        print(f"⏰ Khởi động lúc: {MessageHandler.format_time_message()}")
        self.bot.polling()

    def start_message(self, message):
        """Xử lý lệnh /start"""
        user_id = message.chat.id
        self._clear_user_data(user_id)
        
        text = (
            "🤖 **Chào mừng bạn đến với BéHoà-4o trên Telegram!**\n\n"
            f"{MessageHandler.format_time_message()}\n\n"
            "🔹 Bạn có thể bắt đầu chat ngay.\n"
            "🔹 Sử dụng `/help` để xem hướng dẫn chi tiết.\n"
            "🔹 Lịch sử chat sẽ được lưu, nhưng sẽ bị xóa khi bạn nhập `/start`.\n\n"
            "**📌 Các lệnh thường dùng:**\n"
            "• Gõ tin nhắn bất kỳ để tôi trả lời\n"
            "• `/help` - Xem hướng dẫn đầy đủ\n"
            "• `/clear` - Xóa lịch sử chat\n"
            "• `/time` - Xem thời gian hiện tại\n"
            "• `/vang` - Xem giá vàng SJC và PNJ\n"
            "• `/ngoaite` - Xem tỷ giá ngoại tệ\n"
            "• `/tienao` - Xem giá tiền ảo\n"
            "• `/info` - Xem thông tin của bạn\n" 
            "liên hệ: @smlnobita (Telegram)\n\n"
            "🚀 **Hãy bắt đầu trò chuyện ngay!**"
        )
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🚀 Bắt đầu", callback_data="start"),
            InlineKeyboardButton("🧹 Xóa lịch sử", callback_data="clear")
        )
        
        self.bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

    def time_message(self, message):
        """Xử lý lệnh /time"""
        self.bot.send_message(
            message.chat.id,
            MessageHandler.format_time_message(),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()
