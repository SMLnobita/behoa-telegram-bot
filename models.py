# models.py
from enums import UserStage

class UserState:
    def __init__(self):
        self.message_count = 0
        self.stage = UserStage.INITIAL
        self.last_message_time = 0
        self.waiting_for_key = False