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

    def generate_image(self, prompt: str) -> str:
        """
        Tạo hình ảnh từ mô tả sử dụng DALL-E của OpenAI
        
        Args:
            prompt (str): Mô tả hình ảnh cần tạo
            
        Returns:
            str: URL của hình ảnh được tạo
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",  # Use DALL-E 3 for better quality
                prompt=prompt,
                size="1024x1024",  # Standard size
                quality="standard",
                n=1
            )
            
            return response.data[0].url
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return None