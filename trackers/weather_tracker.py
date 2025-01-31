# trackers/weather_tracker.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import Dict, Optional
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import re

weather_icons = {
    'sunny': '☀️',
    'cloudy': '☁️',
    'rain': '🌧️',
    'storm': '⛈️',
    'snow': '❄️',
    'fog': '🌫️',
    'wind': '💨',
    'clear': '🌙',
    'partly cloudy': '⛅',
    'hazy': '🌤️',
    "Nắng": "☀️", "Mưa": "🌧️", "Mây": "⛅",
    "Bão": "🌪️", "Sương mù": "🌫️", "Giông bão": "⛈️",
    "Nhiều mây": "☁️", "Gió": "💨", "Lạnh": "❄️", "Nóng": "🔥"
}

class WeatherTracker:
    def __init__(self):
        self.base_url = "https://www.accuweather.com/vi/vn"
        self.cities = {
            'tan_an': {'id': '354470', 'name': 'Tân An', 'region': 'Long An'},
            'hcmc': {'id': '353981', 'name': 'TP Hồ Chí Minh', 'region': 'Hồ Chí Minh'},
            'hanoi': {'id': '353412', 'name': 'Hà Nội', 'region': 'Hà Nội'},
            'thu_duc': {'id': '414495', 'name': 'Thủ Đức', 'region': 'Hồ Chí Minh'},
            'di_an': {'id': '352247', 'name': 'Dĩ An', 'region': 'Bình Dương'}
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.logger = logging.getLogger(__name__)

    @lru_cache(maxsize=32)
    def get_city_url(self, city_key: str) -> Optional[str]:
        if city := self.cities.get(city_key):
            city_name = city['name'].lower().replace(' ', '-')
            return f"{self.base_url}/{city_name}/{city['id']}/weather-forecast/{city['id']}"
        return None

    def fetch_city_weather(self, city_key: str) -> Optional[Dict]:
        try:
            city_url = self.get_city_url(city_key)
            if not city_url:
                return None

            response = requests.get(city_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            city = self.cities[city_key]
            current_weather = {
                'location': f"{city['name']}, {city['region']}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }

            if temp := soup.find('div', {'class': 'temp'}):
                current_weather['temperature'] = temp.text.strip()

            if phrase := soup.find('span', {'class': 'phrase'}):
                current_weather['condition'] = phrase.text.strip()

            if air_quality := soup.find('span', {'class': 'air-quality-module__row__category'}):
                current_weather['air_quality'] = air_quality.text.strip()

            return current_weather

        except Exception as e:
            self.logger.error(f"Lỗi khi lấy thời tiết cho {city_key}: {str(e)}")
            return None

    def fetch_weather_data(self) -> Dict:
        weather_data = {}
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_city = {executor.submit(self.fetch_city_weather, city_key): city_key 
                            for city_key in self.cities}
            
            for future in future_to_city:
                city_key = future_to_city[future]
                if result := future.result():
                    weather_data[city_key] = result

        return weather_data
    
    def escape_markdown_v2(self, text: str) -> str:
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

    def format_weather_data(self, weather_data: Dict) -> str:
        lines = [
            "🌤️ *DỰ BÁO THỜI TIẾT HÔM NAY* 🌡️\n",
            f"📅 *Ngày:* `{datetime.now().strftime('%d/%m/%Y')}`\n"
        ]

        for data in weather_data.values():
            condition_icon = next(
                (icon for key, icon in weather_icons.items() if key.lower() in data.get("condition", "").lower()), "🌍"
            )

            # Escape text để tránh lỗi MarkdownV2
            location = self.escape_markdown_v2(data['location'])
            condition = self.escape_markdown_v2(data.get("condition", "N/A"))
            temperature = self.escape_markdown_v2(data.get("temperature", "N/A"))
            air_quality = self.escape_markdown_v2(data.get("air_quality", "N/A"))

            lines.extend([
                f"📍 *{location}*",
                f"   {condition_icon} *➡️ {condition} ⬅️*",
                f"   🌡️ *Nhiệt độ:* *{temperature}*",
                f"   🌬️ *Chất lượng không khí:* *{air_quality}*",
                "──────────────"
            ])

        lines.append(f"🕒 *Cập nhật:* `{datetime.now().strftime('%H:%M:%S')} ⏳` 🇻🇳")

        # Chuyển danh sách thành chuỗi
        message = "\n".join(lines)

        return message
