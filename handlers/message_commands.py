# handlers/message_commands.py
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from config import MessageLimits
from enums import UserStage
from utils.message_handler import MessageHandler

class MessageCommands:
    def __init__(self, bot, user_manager, trackers):
        """
        Initialize MessageCommands with required dependencies
        
        Args:
            bot: Telebot instance
            user_manager: UserManager instance
            trackers: Dictionary containing various trackers (gold, crypto, etc.)
        """
        self.bot = bot
        self.user_manager = user_manager
        self.gold_tracker = trackers['gold']
        self.currency_tracker = trackers['currency']
        self.crypto_tracker = trackers['crypto']
        self.openai_handler = trackers['openai']

    def start_message(self, message):
        """Xử lý lệnh /start"""
        user_id = message.chat.id
        self.user_manager.clear_user_data(user_id)
        
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
            "• `/image <mô tả>` để tạo hình ảnh\n"
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
            "**🎨 Tạo hình ảnh:**\n"
            "• Sử dụng `/image <mô tả>` để tạo hình ảnh\n"
            "• Ví dụ: `/image một chú mèo đang ngủ`\n\n"
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
        
        self.bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    def clear_message(self, message):
        """Xử lý lệnh /clear"""
        user_id = message.chat.id
        self.user_manager.clear_user_data(user_id)
        self.bot.send_message(
            user_id,
            "🧹 **Lịch sử chat đã được xóa!** Bạn có thể tiếp tục chat mới.",
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

    def time_message(self, message):
        """Xử lý lệnh /time"""
        self.bot.send_message(
            message.chat.id,
            MessageHandler.format_time_message(),
            parse_mode="Markdown"
        )

    def image_message(self, message):
        """Xử lý lệnh /image"""
        user_id = message.chat.id
        user_state = self.user_manager.get_user_state(user_id)

        # Kiểm tra giới hạn tin nhắn và thời gian chờ
        if not self.user_manager.can_send_message(user_state):
            self.bot.reply_to(
                message,
                "⏳ **Đợi một chút rồi tạo ảnh tiếp nhé!**",
                parse_mode="Markdown"
            )
            return

        if not self.user_manager.check_message_limit(user_state):
            menu = MessageHandler.create_menu_markup(user_state)
            message_text = "⚠️ **Bạn đã đạt giới hạn tin nhắn cho giai đoạn này!**"
            
            if user_state.stage == UserStage.INITIAL:
                message_text += "\nNhấn 'Tiếp tục nhắn' để được cấp thêm tin nhắn."
            elif user_state.stage == UserStage.EXTENDED:
                message_text += "\nNhập key để được cấp thêm tin nhắn."
            
            self.bot.reply_to(
                message,
                message_text,
                parse_mode="Markdown",
                reply_markup=menu
            )
            return

        try:
            # Extract prompt from message
            if len(message.text.split()) < 2:
                self.bot.reply_to(
                    message,
                    "⚠️ Vui lòng nhập mô tả hình ảnh sau lệnh /image\n" +
                    "Ví dụ: `/image một chú mèo đang ngủ`",
                    parse_mode="Markdown"
                )
                return

            prompt = " ".join(message.text.split()[1:])
            
            # Send "processing" message
            processing_msg = self.bot.reply_to(
                message,
                "🎨 **Đang tạo hình ảnh...**\n" +
                "⏳ Vui lòng đợi trong giây lát!",
                parse_mode="Markdown"
            )

            # Generate image
            image_url = self.openai_handler.generate_image(prompt)
            
            if image_url:
                # Cập nhật số lượt chat
                user_state.last_message_time = time.time()
                user_state.message_count += 1
                
                # Tính số tin nhắn còn lại
                remaining = MessageHandler.get_remaining_messages(user_state)
                
                # Download and send image
                self.bot.delete_message(message.chat.id, processing_msg.message_id)
                self.bot.send_photo(
                    message.chat.id,
                    image_url,
                    caption=f"🎨 *Hình ảnh được tạo từ mô tả:*\n`{prompt}`\n\n💬 Bạn còn {remaining} tin nhắn.",
                    parse_mode="Markdown",
                    reply_to_message_id=message.message_id
                )
            else:
                raise Exception("Không thể tạo hình ảnh")

        except Exception as e:
            error_message = f"❌ Lỗi khi tạo hình ảnh: {str(e)}"
            self.bot.edit_message_text(
                error_message,
                chat_id=message.chat.id,
                message_id=processing_msg.message_id,
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