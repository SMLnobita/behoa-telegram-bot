# utils/message_handler.py
from datetime import datetime
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
        weekday_vn = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][current_time.weekday()]
        return f"🕐 {weekday_vn}, {current_time.strftime('%d/%m/%Y %H:%M:%S')}"

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