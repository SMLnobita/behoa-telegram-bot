import requests
from datetime import datetime
import pytz
from typing import Dict

class CryptoPriceTracker:
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3/ticker/price"
        self.currencies = {
            "BTC": "Bitcoin",
            "ETH": "Ethereum",
            "BNB": "Binance Coin",
            "XRP": "XRP",
            "TRX": "TRON",
            "SOL": "Solana",
            "DOGE": "Dogecoin"
        }

    def fetch_crypto_prices(self) -> Dict:
        try:
            prices = {}
            for symbol, name in self.currencies.items():
                url = f"{self.base_url}?symbol={symbol}USDT"
                response = requests.get(url, timeout=10)
                
                if response.status_code != 200:
                    raise Exception(f"HTTP Error for {symbol}: {response.status_code}")
                
                data = response.json()
                price = float(data["price"])
                
                # Format price based on value
                if price < 1:
                    formatted_price = f"${price:.4f} USD"
                elif price < 100:
                    formatted_price = f"${price:.2f} USD"
                else:
                    formatted_price = f"${price:,.0f} USD"
                
                prices[symbol] = {
                    "name": name,
                    "price": formatted_price
                }
                
            return prices
        except Exception as e:
            raise Exception(f"🚨 Lỗi khi lấy giá tiền ảo: {str(e)}")

    def format_crypto_prices(self, prices: Dict) -> str:
        message = "🚀 **Cập nhật giá tiền điện tử trên Binance**\n\n"
        
        icons = {
            "BTC": "💰",  # Bitcoin - Vàng kỹ thuật số
            "ETH": "⚙️",  # Ethereum - Công nghệ smart contract
            "BNB": "🏦",  # BNB - Biểu tượng tài chính và quyền lực
            "XRP": "💦",  # XRP - Thanh khoản và tốc độ
            "TRX": "🎢",  # TRX - Tốc độ giao dịch nhanh, biểu tượng chuyển động
            "SOL": "🌱",  # SOL - Tăng trưởng mạnh mẽ
            "DOGE": "🚀"   # DOGE - Meme coin bay tới mặt trăng!
        }
        
        for symbol, data in prices.items():
            icon = icons.get(symbol, "💎📊")  # Icon mặc định nếu không có trong danh sách
            message += f"{icon} **{symbol} - {data['name']}**\n"
            message += f"💲💹 Giá: `{data['price']}`\n\n"
        
        current_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        message += f"⏳ **Cập nhật:** `{current_time.strftime('%d/%m/%Y %H:%M:%S')}` 🇻🇳"
        return message


