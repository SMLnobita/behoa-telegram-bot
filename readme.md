# BéHoà-4o Telegram Bot

BéHoà-4o là một chatbot Telegram thông minh được xây dựng với GPT-4o, cung cấp khả năng chat AI và nhiều tính năng hữu ích khác. Bot có thể trò chuyện tự nhiên, tra cứu giá vàng, tỷ giá ngoại tệ và giá tiền ảo theo thời gian thực.

## 🚀 Tính năng chính

- Chat AI thông minh với GPT-4o
- Tra cứu giá vàng SJC và PNJ theo khu vực
- Xem tỷ giá ngoại tệ Vietcombank
- Theo dõi giá tiền ảo từ Binance
- Hệ thống giới hạn tin nhắn theo giai đoạn
- Lưu trữ và quản lý lịch sử chat
- Hỗ trợ đa ngôn ngữ

## 📋 Yêu cầu hệ thống

- Python 3.8+
- pip (Python package manager)

## 🔧 Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/behoa-4o-bot.git
cd behoa-4o-bot
```

2. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env` và cấu hình các biến môi trường:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## 🎯 Cấu trúc dự án

```
behoa-4o-bot/
├── config.py           # Cấu hình và biến môi trường
├── enums.py           # Các enum và hằng số
├── main.py            # File chính của bot
├── models.py          # Các model dữ liệu
├── trackers/          # Các module theo dõi giá
│   ├── crypto_tracker.py
│   ├── currency_tracker.py
│   └── gold_tracker.py
├── utils/             # Các tiện ích
│   ├── message_handler.py
│   └── openai_handler.py
└── history/           # Thư mục lưu lịch sử chat
```

## 💬 Các lệnh hỗ trợ

- `/start` - Khởi động bot và xóa lịch sử chat
- `/help` - Hiển thị hướng dẫn sử dụng
- `/clear` - Xóa lịch sử chat hiện tại
- `/time` - Xem thời gian hiện tại
- `/vang` - Xem giá vàng SJC và PNJ
- `/ngoaite` - Xem tỷ giá ngoại tệ
- `/tienao` - Xem giá tiền ảo

## ⚙️ Giới hạn tin nhắn

Bot sử dụng hệ thống giới hạn tin nhắn 3 giai đoạn:

1. **Giai đoạn 1 (Initial)**:
   - Giới hạn: 10 tin nhắn
   - Có thể mở rộng bằng nút "Tiếp tục nhắn"

2. **Giai đoạn 2 (Extended)**:
   - Giới hạn: 20 tin nhắn
   - Yêu cầu nhập key để tiếp tục

3. **Giai đoạn 3 (Key Used)**:
   - Giới hạn: 35 tin nhắn
   - Giai đoạn cuối cùng

## 🚦 Khởi chạy

Để khởi động bot:

```bash
python main.py
```

## 🔍 Lưu ý

- Thời gian chờ giữa các tin nhắn: 3 giây
- Lịch sử chat được lưu cho đến khi xóa hoặc khởi động lại
- Bot tự động cập nhật thời gian Việt Nam
- Các API được sử dụng:
  - OpenAI API cho GPT-4o
  - Binance API cho giá tiền ảo
  - Vietcombank API cho tỷ giá ngoại tệ
  - PNJ API cho giá vàng

## 🛠️ Phát triển

### Thêm tính năng mới

1. Tạo module mới trong thư mục phù hợp
2. Cập nhật hàm `_register_handlers()` trong `main.py`
3. Thêm logic xử lý trong class `TelegramBot`

### Cập nhật giới hạn tin nhắn

Chỉnh sửa các giá trị trong `config.py`:
```python
class MessageLimits:
    INITIAL_LIMIT = 10
    EXTENDED_LIMIT = 20
    FINAL_LIMIT = 35
    COOLDOWN = 3
    VALID_KEY = "Behoane"
```

## 📄 Giấy phép

[MIT License](https://www.facebook.com/SMLxuneo/)

## 👥 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.