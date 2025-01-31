import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import pytz
from typing import Dict

class CurrencyExchangeTracker:
    def __init__(self):
        self.url = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
        self.currencies = {
            "USD": "🇺🇸 Hoa Kỳ",
            "EUR": "🇪🇺 Liên minh Châu Âu",
            "CNY": "🇨🇳 Trung Quốc",
            "JPY": "🇯🇵 Nhật Bản",
            "KRW": "🇰🇷 Hàn Quốc"
        }

    def fetch_exchange_rates(self) -> Dict:
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            exchange_rates = {}

            for currency_code, country in self.currencies.items():
                for rate in root.findall("Exrate"):
                    if rate.get("CurrencyCode") == currency_code:
                        exchange_rates[currency_code] = {
                            "Quốc gia": country,
                            "Mua tiền mặt": f"{float(rate.get('Buy').replace(',', '')):,.0f} VNĐ",
                            "Mua chuyển khoản": f"{float(rate.get('Transfer').replace(',', '')):,.0f} VNĐ",
                            "Giá bán": f"{float(rate.get('Sell').replace(',', '')):,.0f} VNĐ"
                        }

            return exchange_rates
        except requests.RequestException as e:
            raise Exception(f"⚠️ Lỗi khi lấy tỷ giá: {str(e)}")

    def format_exchange_rates(self, rates: Dict) -> str:
        message = "💹 **Tỷ giá ngoại tệ Vietcombank hôm nay**\n\n"

        for currency, data in rates.items():
            message += f"🌍 **{currency} - {data['Quốc gia']}**\n"
            message += f"💵 Mua tiền mặt: `{data['Mua tiền mặt']}`\n"
            message += f"🏦 Mua chuyển khoản: `{data['Mua chuyển khoản']}`\n"
            message += f"💰 Bán ra: `{data['Giá bán']}`\n\n"

        current_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        message += f"🕒 **Cập nhật:** `{current_time.strftime('%d/%m/%Y %H:%M:%S')}` 🇻🇳"
        return message
