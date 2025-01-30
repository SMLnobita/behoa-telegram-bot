from enum import Enum

class UserStage(Enum):
    INITIAL = 'initial'      # 0-10 tin nhắn
    EXTENDED = 'extended'    # 11-20 tin nhắn (sau khi dùng "Tiếp tục nhắn")
    KEY_USED = 'key_used'    # 21-35 tin nhắn (sau khi nhập key)