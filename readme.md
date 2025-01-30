# 🤖 BéHoà-4o Telegram Bot

**BéHoà-4o** là một chatbot Telegram thông minh sử dụng GPT-4o, cung cấp khả năng trò chuyện tự nhiên cùng nhiều tiện ích như tra cứu giá vàng, tỷ giá ngoại tệ, giá tiền ảo theo thời gian thực, và hiển thị thông tin người dùng.

---

## 🚀 Tính năng chính

✔️ Chat AI thông minh với GPT-4o  
✔️ Tra cứu giá vàng SJC & PNJ theo khu vực  
✔️ Xem tỷ giá ngoại tệ từ Vietcombank  
✔️ Theo dõi giá tiền ảo từ Binance  
✔️ Hệ thống giới hạn tin nhắn theo giai đoạn  
✔️ Lưu trữ và quản lý lịch sử chat  
✔️ Hỗ trợ đa ngôn ngữ  

---

## 🛠 Yêu cầu hệ thống

- **Python** 3.10+
- **pip** (Python package manager)

---

## 🔧 Hướng dẫn cài đặt

1️⃣ **Clone repository**  
```bash
git clone https://github.com/yourusername/behoa-4o-bot.git
cd behoa-telegram-bot
```

2️⃣ **Cài đặt thư viện cần thiết**  
```bash
pip install -r requirements.txt
```

3️⃣ **Cấu hình biến môi trường**  
Tạo file `.env` và thêm thông tin sau:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

---

## 📂 Cấu trúc dự án

```
behoa-telegram-bot/
├── config.py          # Cấu hình và biến môi trường
├── enums.py           # Các enum và hằng số
├── main.py            # File chính của bot
├── models.py          # Các model dữ liệu
├── trackers/          # Theo dõi giá cả
│   ├── crypto_tracker.py
│   ├── currency_tracker.py
│   └── gold_tracker.py
├── utils/             # Tiện ích
│   ├── message_handler.py
│   └── openai_handler.py
└── history/           # Lưu trữ lịch sử chat
```

---

## 💬 Các lệnh hỗ trợ

| Lệnh       | Mô tả |
|------------|------------------------------------------------|
| `/start`   | Khởi động bot & xóa lịch sử chat |
| `/help`    | Hiển thị hướng dẫn sử dụng |
| `/clear`   | Xóa lịch sử chat hiện tại |
| `/time`    | Xem thời gian hiện tại |
| `/info`    | Xem thông tin cá nhân |
| `/vang`    | Xem giá vàng SJC & PNJ |
| `/ngoaite` | Xem tỷ giá ngoại tệ |
| `/tienao`  | Xem giá tiền ảo từ Binance |

---

## ⚙️ Hệ thống giới hạn tin nhắn

BéHoà-4o sử dụng hệ thống giới hạn tin nhắn theo giai đoạn:

🔹 **Giai đoạn 1 (Initial)**  
   - Giới hạn: 10 tin nhắn  
   - Có thể mở rộng bằng nút "Tiếp tục nhắn"

🔹 **Giai đoạn 2 (Extended)**  
   - Giới hạn: 20 tin nhắn  
   - Yêu cầu nhập key để tiếp tục

🔹 **Giai đoạn 3 (Key Used)**  
   - Giới hạn: 35 tin nhắn  
   - Giai đoạn cuối cùng

---

## 🚀 Khởi chạy bot

```bash
python main.py
```

---

## 🔍 Lưu ý

✔️ Thời gian chờ giữa các tin nhắn: **3 giây**  
✔️ Lịch sử chat được lưu cho đến khi xóa hoặc khởi động lại  
✔️ Bot tự động cập nhật theo **giờ Việt Nam**  
✔️ API được sử dụng:  
   - **OpenAI API** (GPT-4o)  
   - **Binance API** (Giá tiền ảo)  
   - **Vietcombank API** (Tỷ giá ngoại tệ)  
   - **PNJ API** (Giá vàng)

---

## 🛠 Phát triển

### 📌 Thêm tính năng mới

1️⃣ Tạo module mới trong thư mục phù hợp  
2️⃣ Cập nhật hàm `_register_handlers()` trong `main.py`  
3️⃣ Thêm logic xử lý trong class `TelegramBot`

### ⚙️ Cập nhật giới hạn tin nhắn

Chỉnh sửa các giá trị trong `config.py`:
```python
class MessageLimits:
    INITIAL_LIMIT = 10
    EXTENDED_LIMIT = 20
    FINAL_LIMIT = 35
    COOLDOWN = 3
    VALID_KEY = "Behoane"
```

---

## 📄 Giấy phép

Dự án được phát hành theo [MIT License](https://www.facebook.com/SMLxuneo/).

---

## 🤝 Đóng góp

💡 Mọi đóng góp đều được chào đón!  
Vui lòng tạo **Issue** hoặc **Pull Request** trên GitHub.
