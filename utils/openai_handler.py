# utils/openai_handler.py
import openai
from config import Config

class OpenAIHandler:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    def process_message(self, messages, time_info):
        try:
            # Thêm thông tin thời gian vào system message
            system_message = f"Bạn là một chatbot AI sử dụng GPT-4o. {time_info}"
            messages[0]["content"] = system_message
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Lỗi API OpenAI: {str(e)}"