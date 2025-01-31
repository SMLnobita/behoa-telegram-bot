# handlers/chat_handler.py
import time
import keywords
from config import MessageLimits
from enums import UserStage
from telebot.types import ForceReply
from utils.message_handler import MessageHandler

class ChatHandler:
    def __init__(self, bot, user_manager, trackers):
        """
        Initialize ChatHandler with required dependencies
        
        Args:
            bot: Telebot instance
            user_manager: UserManager instance
            trackers: Dictionary containing various trackers and handlers
        """
        self.bot = bot
        self.user_manager = user_manager
        self.gold_tracker = trackers['gold']
        self.currency_tracker = trackers['currency']
        self.crypto_tracker = trackers['crypto']
        self.weather_tracker = trackers['weather']
        self.openai_handler = trackers['openai']

    def handle_message(self, message):
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            message: Message object từ Telegram
        """
        user_id = message.chat.id
        user_state = self.user_manager.get_user_state(user_id)

        if not self._handle_key_input(message, user_state):
            return

        if not self._check_limits(message, user_id, user_state):
            return

        if self._handle_keywords(message, user_id):
            return

        self._process_chat_message(message, user_id, user_state)

    def _handle_key_input(self, message, user_state):
        """
        Xử lý tin nhắn khi người dùng đang nhập key
        
        Returns:
            bool: True nếu tiếp tục xử lý tin nhắn, False nếu dừng lại
        """
        if user_state.waiting_for_key:
            if message.text == MessageLimits.VALID_KEY:
                user_state.stage = UserStage.KEY_USED
                user_state.waiting_for_key = False
                remaining = MessageLimits.FINAL_LIMIT - user_state.message_count
                self.bot.send_message(
                    message.chat.id, 
                    f"✅ Key hợp lệ! Bạn đã được cấp thêm {remaining} tin nhắn."
                )
            else:
                # Hiển thị thông báo lỗi và menu với nút nhập key
                user_state.waiting_for_key = False
                menu = MessageHandler.create_menu_markup(user_state)
                self.bot.send_message(
                    message.chat.id,
                    "❌ Key không hợp lệ!\n🔑 Vui lòng thử lại.\n🧹 Clear xoá history để chat tiếp",
                    reply_markup=menu
                )
            return False
        return True

    def _check_limits(self, message, user_id, user_state):
        """
        Kiểm tra giới hạn tin nhắn và thời gian chờ
        
        Returns:
            bool: True nếu trong giới hạn cho phép, False nếu vượt giới hạn
        """
        if not self.user_manager.can_send_message(user_state):
            self.bot.send_message(
                user_id,
                "⏳ **Đợi một chút rồi hỏi tiếp nhé!**",
                parse_mode="Markdown"
            )
            return False

        if not self.user_manager.check_message_limit(user_state):
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
            return False

        return True

    def _handle_keywords(self, message, user_id):
        """
        Xử lý các từ khóa trong tin nhắn
        
        Returns:
            bool: True nếu đã xử lý từ khóa, False nếu không có từ khóa
        """
        text = message.text.lower()
        #user_id = message.chat.id

        # Xử lý từ khóa về giá vàng
        if any(keyword in text for keyword in keywords.gold_keywords):
            try:
                # Gửi tin nhắn đang xử lý
                processing_msg = self.bot.reply_to(
                    message,
                    "💰 **Đang lấy dữ liệu giá vàng...**\n" +
                    "⏳ Vui lòng đợi trong giây lát!",
                    parse_mode="Markdown"
                )
                # Lấy dữ liệu và định dạng giá vàng
                gold_data = self.gold_tracker.fetch_gold_prices()
                formatted_message = self.gold_tracker.format_gold_prices(gold_data)
                # Xoá tin nhắn đang xử lý
                self.bot.delete_message(
                    chat_id=user_id,
                    message_id=processing_msg.message_id
                )
                # Gửi dữ liệu giá vàng
                self.bot.send_message(
                    user_id,
                    formatted_message,
                    parse_mode="Markdown",
                    reply_to_message_id=message.message_id
                )
                return True
            except Exception as e:
                self.bot.send_message(user_id, f"❌ {str(e)}")
                return True

        # Xử lý từ khóa về tên bot
        if any(keyword in text for keyword in keywords.name_keywords):
            self.bot.send_message(
                user_id,
                "🤖 **Mình là BéHoà-4o, một chatbot AI thông minh và thân thiện!**",
                parse_mode="Markdown",
                reply_to_message_id=message.message_id
            )
            return True

        # Xử lý từ khóa về ngoại tệ
        if any(keyword in text for keyword in keywords.ngoaite_keywords):
            try:
                # Gửi tin nhắn đang xử lý
                processing_msg = self.bot.reply_to(
                    message,
                    "💱 **Đang lấy dữ liệu tỷ giá ngoại tệ...**\n" +
                    "⏳ Vui lòng đợi trong giây lát!",
                    parse_mode="Markdown"
                )
                # Lấy dữ liệu và định dạng tỷ giá ngoại tệ
                rates = self.currency_tracker.fetch_exchange_rates()
                formatted_message = self.currency_tracker.format_exchange_rates(rates)
                # Xoá tin nhắn đang xử lý
                self.bot.delete_message(
                    chat_id=user_id,
                    message_id=processing_msg.message_id
                )
                # Gửi dữ liệu tỷ giá ngoại tệ
                self.bot.send_message(
                    user_id,
                    formatted_message,
                    parse_mode="Markdown",
                    reply_to_message_id=message.message_id
                )
                return True
            except Exception as e:
                self.bot.send_message(user_id, f"❌ {str(e)}")
                return True

        # Xử lý từ khóa về thời gian
        if any(keyword in text for keyword in keywords.thoigian_keywords):
            self.bot.send_message(
                user_id,
                MessageHandler.format_time_message(),
                parse_mode="Markdown",
                reply_to_message_id=message.message_id
            )
            return True

        # Xử lý từ khóa về tiền ảo
        if any(keyword in text for keyword in keywords.tienao_keywords):
            try:
                #Gửi tin nhắn đang xử lý
                processing_msg = self.bot.reply_to(
                    message,
                    "💰 **Đang lấy dữ liệu giá tiền ảo...**\n" +
                    "⏳ Vui lòng đợi trong giây lát!",
                    parse_mode="Markdown"
                )
                # Lấy dữ liệu và định dạng giá tiền ảo
                crypto_data = self.crypto_tracker.fetch_crypto_prices()
                formatted_message = self.crypto_tracker.format_crypto_prices(crypto_data)
                # Xoá tin nhắn đang xử lý
                self.bot.delete_message(
                    chat_id=user_id,
                    message_id=processing_msg.message_id
                )
                # Gửi dữ liệu giá tiền ảo
                self.bot.send_message(
                    user_id,
                    formatted_message,
                    parse_mode="Markdown",
                    reply_to_message_id=message.message_id
                )
                return True
            except Exception as e:
                self.bot.send_message(user_id, f"❌ {str(e)}")
                return True
            
        # Xử lý từ khoá về thời tiết
        if any(keyword in text for keyword in keywords.thoitiet_keywords):
            try:
                #Gửi tin nhắn đang xử lý
                processing_msg = self.bot.reply_to(
                    message,
                    "🌡️ **Đang lấy dữ liệu thời tiết...**\n" +
                    "⏳ Vui lòng đợi trong giây lát!",
                    parse_mode="Markdown"
                )
                #Lấy và định dạng dữ liệu thời tiết
                weather_data = self.weather_tracker.fetch_weather_data()
                formatted_message = self.weather_tracker.format_weather_data(weather_data)
                #Xoá tin nhắn đang xử lý
                self.bot.delete_message(
                    chat_id=user_id,
                    message_id=processing_msg.message_id
                )
                #Gửi dữ liệu thời tiết
                self.bot.send_message(
                    user_id,
                    formatted_message,
                    parse_mode="Markdown",
                    reply_to_message_id=message.message_id
                )
                return True
            except Exception as e:
                self.bot.send_message(user_id, f"❌ {str(e)}")
                return True
            
        # Xử lý từ khóa về người tạo bot
        if any(keyword in text for keyword in keywords.taohoa_keywords):
            self.bot.send_message(
                user_id,
                "🤖 **Mình là BéHoà-4o, một chatbot AI thông minh và thân thiện!**\n"
                "🤖 **Mình được tạo ra bởi @smlnobita!**",
                parse_mode="Markdown",
                reply_to_message_id=message.message_id
            )
            return True

        return False
    

    def _process_chat_message(self, message, user_id, user_state):
        """Xử lý tin nhắn chat thông thường với OpenAI"""
        user_state.last_message_time = time.time()
        user_state.message_count += 1

        chat_history = MessageHandler.get_chat_history(user_id)
        messages = [{"role": "system", "content": "Bạn là một chatbot AI thông minh và thân thiện."}]

        # Xử lý lịch sử chat
        for chat in chat_history:
            if ": " in chat:
                try:
                    role, content = chat.split(": ", 1)
                    if role in ["user", "assistant", "system"]:
                        messages.append({"role": role, "content": content})
                except ValueError:
                    continue

        # Thêm tin nhắn hiện tại
        messages.append({"role": "user", "content": message.text})
        MessageHandler.add_to_chat_history(user_id, "user", message.text)

        # Lấy thông tin thời gian
        time_info = MessageHandler.format_time_message()
        
        # Xử lý với OpenAI
        reply = self.openai_handler.process_message(messages, time_info)
        MessageHandler.add_to_chat_history(user_id, "assistant", reply)

        # Tính số tin nhắn còn lại
        remaining = MessageHandler.get_remaining_messages(user_state)
        remaining_msg = f"\n\n💬 Bạn còn {remaining} tin nhắn."
        
        # Tạo menu nếu cần
        menu = MessageHandler.create_menu_markup(user_state)
        full_reply = f"{reply}{remaining_msg}"
        
        # Gửi tin nhắn phản hồi
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