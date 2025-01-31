# handlers/callback_handler.py
from telebot.types import ForceReply
from config import MessageLimits
from enums import UserStage
from utils.message_handler import MessageHandler

class CallbackHandler:
    def __init__(self, bot, user_manager):
        """
        Initialize CallbackHandler with required dependencies
        
        Args:
            bot: Telebot instance
            user_manager: UserManager instance
        """
        self.bot = bot
        self.user_manager = user_manager

    def handle_callback(self, call):
        """
        Xử lý callback từ các nút inline keyboard

        Args:
            call: Callback query object từ Telegram
        """
        try:
            user_id = call.message.chat.id
            user_state = self.user_manager.get_user_state(user_id)

            # Xử lý các loại callback khác nhau
            if call.data == "start":
                self._handle_start_callback(user_id)
                
            elif call.data == "clear":
                self._handle_clear_callback(user_id)
                
            elif call.data == "continue":
                self._handle_continue_callback(user_id, user_state)
                
            elif call.data == "request_key":
                self._handle_request_key_callback(user_id, user_state)

            # Xóa nút sau khi xử lý (tùy chọn)
            try:
                self.bot.edit_message_reply_markup(
                    chat_id=user_id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
            except Exception:
                pass

            # Kết thúc callback query
            self.bot.answer_callback_query(call.id)

        except Exception as e:
            error_message = f"❌ Lỗi xử lý callback: {str(e)}"
            self.bot.send_message(
                user_id,
                error_message,
                parse_mode="Markdown"
            )
            self.bot.answer_callback_query(
                call.id,
                text="Có lỗi xảy ra, vui lòng thử lại sau."
            )

    def _handle_clear_callback(self, user_id):
        """Xử lý callback khi nhấn nút 'Xóa lịch sử'"""
        self.user_manager.clear_user_data(user_id)
        self.bot.send_message(
            user_id,
            "🧹 **Lịch sử chat đã được xóa!** Bạn có thể tiếp tục chat mới.",
            parse_mode="Markdown"
        )

    def _handle_continue_callback(self, user_id, user_state):
        """
        Xử lý callback khi nhấn nút 'Tiếp tục nhắn'
        
        Args:
            user_id: ID của người dùng
            user_state: Trạng thái hiện tại của người dùng
        """
        if user_state.stage == UserStage.INITIAL:
            user_state.stage = UserStage.EXTENDED
            remaining = MessageLimits.EXTENDED_LIMIT - user_state.message_count
            self.bot.send_message(
                user_id, 
                f"✨ Bạn đã được cấp thêm {remaining} tin nhắn!"
            )
        else:
            self.bot.send_message(
                user_id,
                "⚠️ Không thể thực hiện thao tác này ở giai đoạn hiện tại."
            )

    def _handle_request_key_callback(self, user_id, user_state):
        """
        Xử lý callback khi nhấn nút 'Nhập key'
        
        Args:
            user_id: ID của người dùng
            user_state: Trạng thái hiện tại của người dùng
        """
        if user_state.stage == UserStage.EXTENDED:
            user_state.waiting_for_key = True
            self.bot.send_message(
                user_id,
                "🔑 Vui lòng nhập key để được cấp thêm tin nhắn:",
                reply_markup=ForceReply()
            )
        else:
            self.bot.send_message(
                user_id,
                "⚠️ Không thể thực hiện thao tác này ở giai đoạn hiện tại."
            )

    def _handle_start_callback(self, user_id):
        """Xử lý callback khi nhấn nút 'Bắt đầu'"""
        self.bot.send_message(
            user_id,
            "💬 Hãy bắt đầu chat!"
        )