# managers/user_manager.py
import time
import os
from models import UserState
from config import Config, MessageLimits
from enums import UserStage
from utils.message_handler import MessageHandler

class UserManager:
    def __init__(self):
        """Initialize UserManager with an empty users dictionary"""
        self.users = {}
        self._ensure_history_directory()

    def _ensure_history_directory(self):
        """Đảm bảo thư mục lưu trữ lịch sử tồn tại"""
        if not os.path.exists(Config.HISTORY_DIR):
            os.makedirs(Config.HISTORY_DIR)

    def get_user_state(self, user_id):
        """
        Lấy hoặc tạo mới trạng thái người dùng
        
        Args:
            user_id: ID của người dùng
            
        Returns:
            UserState: Trạng thái của người dùng
        """
        if user_id not in self.users:
            self.users[user_id] = UserState()
        return self.users[user_id]

    def clear_user_data(self, user_id):
        """
        Xóa toàn bộ dữ liệu của người dùng
        
        Args:
            user_id: ID của người dùng
        """
        MessageHandler.clear_chat_history(user_id)
        self.users[user_id] = UserState()

    def can_send_message(self, user_state):
        """
        Kiểm tra xem người dùng có thể gửi tin nhắn không dựa trên cooldown
        
        Args:
            user_state: Trạng thái của người dùng
            
        Returns:
            bool: True nếu có thể gửi tin nhắn, False nếu đang trong thời gian chờ
        """
        current_time = time.time()
        return current_time - user_state.last_message_time >= MessageLimits.COOLDOWN

    def check_message_limit(self, user_state):
        """
        Kiểm tra giới hạn tin nhắn dựa trên trạng thái
        
        Args:
            user_state: Trạng thái của người dùng
            
        Returns:
            bool: True nếu chưa đạt giới hạn, False nếu đã đạt giới hạn
        """
        count = user_state.message_count
        stage = user_state.stage

        if stage == UserStage.INITIAL and count >= MessageLimits.INITIAL_LIMIT:
            return False
        elif stage == UserStage.EXTENDED and count >= MessageLimits.EXTENDED_LIMIT:
            return False
        elif stage == UserStage.KEY_USED and count >= MessageLimits.FINAL_LIMIT:
            return False
        return True

    def update_message_count(self, user_state):
        """
        Cập nhật số lượng tin nhắn và thời gian gửi tin nhắn cuối cùng
        
        Args:
            user_state: Trạng thái của người dùng
        """
        user_state.message_count += 1
        user_state.last_message_time = time.time()

    def get_remaining_messages(self, user_state):
        """
        Tính số tin nhắn còn lại dựa trên trạng thái hiện tại
        
        Args:
            user_state: Trạng thái của người dùng
            
        Returns:
            int: Số tin nhắn còn lại
        """
        stage = user_state.stage
        count = user_state.message_count
        
        if stage == UserStage.INITIAL:
            return max(0, MessageLimits.INITIAL_LIMIT - count)
        elif stage == UserStage.EXTENDED:
            return max(0, MessageLimits.EXTENDED_LIMIT - count)
        elif stage == UserStage.KEY_USED:
            return max(0, MessageLimits.FINAL_LIMIT - count)
        return 0

    def upgrade_user_stage(self, user_state):
        """
        Nâng cấp giai đoạn của người dùng
        
        Args:
            user_state: Trạng thái của người dùng
            
        Returns:
            bool: True nếu nâng cấp thành công, False nếu không thể nâng cấp
        """
        if user_state.stage == UserStage.INITIAL:
            user_state.stage = UserStage.EXTENDED
            return True
        elif user_state.stage == UserStage.EXTENDED and not user_state.waiting_for_key:
            user_state.waiting_for_key = True
            return True
        return False

    def verify_key(self, user_state, key):
        """
        Xác thực key và cập nhật trạng thái nếu hợp lệ
        
        Args:
            user_state: Trạng thái của người dùng
            key: Key được nhập
            
        Returns:
            bool: True nếu key hợp lệ, False nếu không hợp lệ
        """
        if user_state.stage == UserStage.EXTENDED and key == MessageLimits.VALID_KEY:
            user_state.stage = UserStage.KEY_USED
            user_state.waiting_for_key = False
            return True
        return False

    def get_chat_history(self, user_id):
        """
        Lấy lịch sử chat của người dùng
        
        Args:
            user_id: ID của người dùng
            
        Returns:
            list: Danh sách các tin nhắn trong lịch sử
        """
        return MessageHandler.get_chat_history(user_id)

    def add_to_chat_history(self, user_id, role, content):
        """
        Thêm tin nhắn vào lịch sử chat
        
        Args:
            user_id: ID của người dùng
            role: Vai trò của người gửi tin nhắn
            content: Nội dung tin nhắn
        """
        MessageHandler.add_to_chat_history(user_id, role, content)

    def get_stage_info(self, user_state):
        """
        Lấy thông tin về giai đoạn hiện tại của người dùng
        
        Args:
            user_state: Trạng thái của người dùng
            
        Returns:
            dict: Thông tin về giai đoạn hiện tại
        """
        stage = user_state.stage
        count = user_state.message_count
        
        if stage == UserStage.INITIAL:
            return {
                "current_stage": "Giai đoạn 1",
                "message_limit": MessageLimits.INITIAL_LIMIT,
                "remaining": self.get_remaining_messages(user_state),
                "can_upgrade": count >= MessageLimits.INITIAL_LIMIT
            }
        elif stage == UserStage.EXTENDED:
            return {
                "current_stage": "Giai đoạn 2",
                "message_limit": MessageLimits.EXTENDED_LIMIT,
                "remaining": self.get_remaining_messages(user_state),
                "can_upgrade": count >= MessageLimits.EXTENDED_LIMIT
            }
        else:
            return {
                "current_stage": "Giai đoạn 3",
                "message_limit": MessageLimits.FINAL_LIMIT,
                "remaining": self.get_remaining_messages(user_state),
                "can_upgrade": False
            }