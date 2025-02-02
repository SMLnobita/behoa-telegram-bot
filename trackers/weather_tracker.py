import requests
from datetime import datetime
import pytz
from typing import Dict, Tuple
from config import Config

class WeatherAirQualityTracker:
    def __init__(self):
        """Initialize the weather and air quality tracker"""
        self.api_key = "46d84154e0037a53ad8727fb9ea7e493"
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.air_quality_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        
        # Map of supported cities
        self.cities = {
            "Tân An": {
                "id": 1567069,
                "region": "Long An",
                "lat": 10.5333,
                "lon": 106.4167
            },
            "TP Hồ Chí Minh": {
                "id": 1566083,
                "region": "Hồ Chí Minh",
                "lat": 10.75,
                "lon": 106.6667
            },
            "Hà Nội": {
                "id": 1581130,
                "region": "Hà Nội",
                "lat": 21.0245,
                "lon": 105.8412
            }
        }

        # Weather condition icons mapping
        self.weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Smoke": "🌫️",
            "Haze": "🌫️",
            "Dust": "🌫️",
            "Fog": "🌫️",
            "Sand": "🌫️",
            "Ash": "🌫️",
            "Squall": "🌪️",
            "Tornado": "🌪️"
        }

        # US AQI breakpoints for PM2.5
        self.pm25_breakpoints = [
            (0.0, 12.0, 0, 50, "Tốt 🌱"),
            (12.1, 35.4, 51, 100, "Trung bình 😃"),
            (35.5, 55.4, 101, 150, "Không tốt cho nhóm nhạy cảm 😷"),
            (55.5, 150.4, 151, 200, "Không tốt cho sức khỏe 🤢"),
            (150.5, 250.4, 201, 300, "Rất không tốt cho sức khỏe ☠️"),
            (250.5, 500.4, 301, 500, "Nguy hiểm 🏭"),
        ]

    def _calculate_vn_aqi(self, pm25: float) -> Tuple[int, str]:
        """
        Calculate US AQI from PM2.5 concentration
        
        Args:
            pm25 (float): PM2.5 concentration in µg/m³
            
        Returns:
            Tuple[int, str]: US AQI value and description
        """
        for low_c, high_c, low_i, high_i, description in self.pm25_breakpoints:
            if low_c <= pm25 <= high_c:
                aqi = round(((high_i - low_i) / (high_c - low_c)) * (pm25 - low_c) + low_i)
                return aqi, description
        
        # If PM2.5 is above the highest breakpoint
        if pm25 > 500.4:
            return 500, "Nguy hiểm 🟤"
        # If PM2.5 is below the lowest breakpoint
        return 0, "Tốt 🟢"

    def fetch_weather_data(self) -> Dict:
        """
        Fetch weather and air quality data for all configured cities
        
        Returns:
            Dict: Weather and air quality data for each city
        """
        try:
            weather_data = {}
            
            for city_name, city_info in self.cities.items():
                try:
                    # Get weather data
                    weather_response = self._fetch_weather(city_info['id'])
                    
                    # Get air quality data
                    air_quality_response = self._fetch_air_quality(
                        city_info['lat'], 
                        city_info['lon']
                    )
                    
                    # Get PM2.5 value
                    pm25 = air_quality_response['list'][0]['components']['pm2_5']
                    
                    # Calculate US AQI
                    vn_aqi, vn_aqi_desc = self._calculate_vn_aqi(pm25)
                    
                    # Combine the data
                    weather_data[city_name] = {
                        "location": f"{city_name}, {city_info['region']}",
                        "temperature": f"{round(weather_response['main']['temp'])}°C",
                        "feels_like": f"{round(weather_response['main']['feels_like'])}°C",
                        "humidity": f"{weather_response['main']['humidity']}%",
                        "wind_speed": f"{round(weather_response['wind']['speed'] * 3.6, 1)} km/h",
                        "condition": weather_response['weather'][0]['description'].capitalize(),
                        "condition_main": weather_response['weather'][0]['main'],
                        "air_quality": self._get_air_quality_description(
                            air_quality_response['list'][0]['main']['aqi']
                        ),
                        "pm25": f"{round(pm25, 1)}",
                        "vn_aqi": f"{vn_aqi}",
                        "vn_aqi_desc": vn_aqi_desc,
                        "timestamp": datetime.now(Config.VN_TIMEZONE).strftime('%H:%M:%S')
                    }

                except Exception as e:
                    print(f"Error fetching data for {city_name}: {str(e)}")
                    continue
            
            if not weather_data:
                raise Exception("Không thể lấy dữ liệu thời tiết cho bất kỳ thành phố nào")
            
            return weather_data
            
        except Exception as e:
            raise Exception(f"🚨 Lỗi khi lấy dữ liệu thời tiết: {str(e)}")

    def _fetch_weather(self, city_id: int) -> Dict:
        """Fetch weather data for a specific city"""
        try:
            response = requests.get(
                self.weather_url,
                params={
                    "id": city_id,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "vi"
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Lỗi khi lấy dữ liệu thời tiết: {str(e)}")

    def _fetch_air_quality(self, lat: float, lon: float) -> Dict:
        """Fetch air quality data for specific coordinates"""
        try:
            response = requests.get(
                self.air_quality_url,
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.api_key
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Lỗi khi lấy dữ liệu chất lượng không khí: {str(e)}")

    def _get_air_quality_description(self, aqi: int) -> str:
        """Convert AQI number to descriptive text"""
        descriptions = {
            1: "Tốt",
            2: "Khá",
            3: "Trung bình",
            4: "Kém",
            5: "Rất xấu"
        }
        return descriptions.get(aqi, "Không xác định ⚪")

    def format_weather_data(self, weather_data: Dict) -> str:
        """Format weather data into a readable message"""
        try:
            message = [
                "🌤️ **BẢN TIN THỜI TIẾT & CHẤT LƯỢNG KHÔNG KHÍ**\n",
                f"🕒 Cập nhật lúc `{datetime.now(Config.VN_TIMEZONE).strftime('%H:%M:%S')}` 🇻🇳\n"
            ]

            for city_name, data in weather_data.items():
                # Get weather icon
                icon = self.weather_icons.get(data['condition_main'], "🌡️")
                
                # Format city data
                city_info = [
                    f"📍 **{data['location']}**",
                    f"{icon} {data['condition']}",
                    f"🌡️ Nhiệt độ: `{data['temperature']}`",
                    f"🌡️ Cảm giác như: `{data['feels_like']}`",
                    f"💧 Độ ẩm: `{data['humidity']}`",
                    f"💨 Tốc độ gió: `{data['wind_speed']}`",
                    f"🌬️ Chất lượng không khí: `{data['air_quality']}`",
                    f"🇻🇳 Chỉ số AQI: `{data['vn_aqi']} - {data['vn_aqi_desc']}`",
                    f"😷 Nồng độ PM2.5: `{data['pm25']} µg/m³`\n"
                ]
                message.extend(city_info)

            return "\n".join(message)
        except Exception as e:
            raise Exception(f"Lỗi khi định dạng dữ liệu thời tiết: {str(e)}")