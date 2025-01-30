# utils/message_handler.py
from datetime import datetime
import lunarcalendar
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import os
from config import Config, MessageLimits
from enums import UserStage

class MessageHandler:
    @staticmethod
    def get_current_time_vn():
        return datetime.now(Config.VN_TIMEZONE)

    @staticmethod
    def format_time_message():
        current_time = MessageHandler.get_current_time_vn()
        WEEKDAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
        weekday_vn = WEEKDAYS[current_time.weekday()]
        
        # Chuyển đổi sang lịch âm
        lunar_date = lunarcalendar.Converter.Solar2Lunar(current_time)
        
        # Lấy múi giờ UTC
        utc_offset = current_time.strftime('%z')
        hours_offset = int(utc_offset[:-2]) if utc_offset else 7  # Mặc định UTC+7 nếu không có

        return (
            f"🕐 **{weekday_vn},** `ngày {current_time.day:02d} tháng {current_time.month:02d} năm {current_time.year}`\n"
            f"⏰ **Giờ:** `{current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}`\n"
            f"🌙 **Âm lịch:** `Ngày {lunar_date.day:02d} tháng {lunar_date.month:02d} năm {lunar_date.year}`\n"
            f"🌍 **Múi giờ:** `UTC{'+' if hours_offset >= 0 else ''}{hours_offset}`"
        )

    @staticmethod
    def create_menu_markup(user_state):
        markup = InlineKeyboardMarkup(row_width=2)
        count = user_state.message_count
        stage = user_state.stage

        if count >= MessageLimits.INITIAL_LIMIT and stage == UserStage.INITIAL:
            markup.add(
                InlineKeyboardButton("Tiếp tục nhắn", callback_data="continue"),
                InlineKeyboardButton("🧹 Clear", callback_data="clear")
            )
            return markup
        elif count >= MessageLimits.EXTENDED_LIMIT and stage == UserStage.EXTENDED:
            markup.add(
                InlineKeyboardButton("Nhập key", callback_data="request_key"),
                InlineKeyboardButton("🧹 Clear", callback_data="clear")
            )
            return markup
        elif count >= MessageLimits.FINAL_LIMIT and stage == UserStage.KEY_USED:
            markup.add(InlineKeyboardButton("🧹 Clear", callback_data="clear"))
            return markup
        return None

    @staticmethod
    def get_chat_history(user_id):
        file_path = f"{Config.HISTORY_DIR}/history_{user_id}.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return []

    @staticmethod
    def add_to_chat_history(user_id, role, content):
        file_path = f"{Config.HISTORY_DIR}/history_{user_id}.txt"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{role}: {content}\n")

    @staticmethod
    def clear_chat_history(user_id):
        file_path = f"{Config.HISTORY_DIR}/history_{user_id}.txt"
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def get_remaining_messages(user_state):
        count = user_state.message_count
        stage = user_state.stage
        
        if stage == UserStage.INITIAL:
            return MessageLimits.INITIAL_LIMIT - count
        elif stage == UserStage.EXTENDED:
            return MessageLimits.EXTENDED_LIMIT - count
        elif stage == UserStage.KEY_USED:
            return MessageLimits.FINAL_LIMIT - count
        return 0