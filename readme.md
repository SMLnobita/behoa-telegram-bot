# 🤖 BéHoà-GPT Telegram Bot

BéHoà-GPT là một chatbot Telegram thông minh, được phát triển bằng Python, tích hợp **GPT-4o-mini** để hỗ trợ trò chuyện và nhiều tính năng hữu ích khác.

## ✨ Tính Năng Chính

- 💬 **Chat Thông Minh** - Tích hợp GPT-4o cho trò chuyện tự nhiên
- 🎨 **Tạo Hình Ảnh** - Tạo hình ảnh bằng DALL·E 3
- 💰 **Theo Dõi Giá Vàng** - Cập nhật giá vàng SJC & PNJ theo thời gian thực
- 💱 **Tỷ Giá Ngoại Tệ** - Tỷ giá Vietcombank cập nhật liên tục
- 🪙 **Giá Tiền Ảo** - Giá tiền điện tử từ Binance theo thời gian thực
- 🌡️ **Thông Tin Thời Tiết** - Thời tiết và chất lượng không khí hiện tại
- ⏰ **Thông Tin Thời Gian** - Cả lịch Dương và Âm

## 🛠️ Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Telegram Bot Token
- OpenAI API Key
- Các gói Python cần thiết (xem `requirements.txt`)

## ⚡ Hướng Dẫn Cài Đặt

1. **Tải source code về máy**
```bash
git clone https://github.com/SMLnobita/behoa-telegram-bot.git
cd behoa-telegram-bot
```

2. **Cài đặt thư viện**
```bash
pip install -r requirements.txt
```

3. **Thiết lập biến môi trường**
Tạo file `.env` với nội dung:
```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

4. **Khởi chạy bot**
```bash
python main.py
```

## 🤖 Các Lệnh Bot

| Lệnh | Mô Tả |
|---------|-------------|
| `/start` | Khởi động bot và xóa lịch sử chat |
| `/help` | Xem hướng dẫn sử dụng |
| `/clear` | Xóa lịch sử chat hiện tại |
| `/time` | Xem thời gian hiện tại (cả 2 lịch) |
| `/info` | Xem thông tin người dùng |
| `/image <mô tả>` | Tạo hình ảnh từ mô tả |
| `/vang` | Xem giá vàng |
| `/ngoaite` | Xem tỷ giá ngoại tệ |
| `/tienao` | Xem giá tiền ảo |
| `/thoitiet` | Xem thời tiết và chất lượng không khí |

## 🔄 Hệ Thống Giới Hạn Tin Nhắn

Bot có cơ chế giới hạn tin nhắn theo các giai đoạn:

| Giai Đoạn | Số Tin Nhắn | Điều Kiện |
|-------|----------|-----------|
| 1️⃣ Ban Đầu | 5 tin nhắn | Mặc định |
| 2️⃣ Mở Rộng | 10 tin nhắn | Sau khi nhấn "Tiếp tục nhắn" |
| 3️⃣ Premium | 15 tin nhắn | Sau khi nhập key |

- ⏱️ Thời gian chờ giữa các tin nhắn: 3 giây
- 🔑 Key để mở khóa giai đoạn Premium: "Behoane"

## 📁 Cấu Trúc Dự Án

```
behoa-telegram-bot/
├── config.py             # Cấu hình môi trường
├── enums.py              # Định nghĩa enum
├── keywords.py           # Danh sách từ khóa
├── main.py               # Điểm khởi đầu ứng dụng
├── models.py             # Các model dữ liệu
│
├── handlers/             # Xử lý tin nhắn
│   ├── callback_handler.py
│   ├── chat_handler.py
│   └── message_commands.py
│
├── managers/             # Quản lý trạng thái
│   └── user_manager.py
│
├── trackers/            # Theo dõi giá cả
│   ├── crypto_tracker.py
│   ├── currency_tracker.py
│   ├── gold_tracker.py
│   └── weather_tracker.py
│
└── utils/               # Tiện ích
    ├── message_handler.py
    └── openai_handler.py
```

## 🌟 Chi Tiết Tính Năng

### 💬 Chat Thông Minh
- Xử lý ngôn ngữ tự nhiên với GPT-4o
- Hội thoại theo ngữ cảnh
- Hỗ trợ đa ngôn ngữ
- Quản lý lịch sử tin nhắn

### 🎨 Tạo Hình Ảnh
- Sử dụng DALL·E 3
- Mô tả bằng ngôn ngữ tự nhiên
- Chất lượng hình ảnh cao
- Đa dạng phong cách và ngữ cảnh

### 💹 Thông Tin Tài Chính
- Giá vàng theo thời gian thực (SJC & PNJ)
- Tỷ giá ngoại tệ cập nhật liên tục
- Dữ liệu thị trường tiền điện tử
- Cập nhật giá thường xuyên

### ⏰ Thời Gian và Thời Tiết
- Hệ thống lịch kép (Dương lịch & Âm lịch)
- Thời tiết nhiều thành phố
- Thông tin chất lượng không khí
- Cập nhật thường xuyên

## 🤝 Đóng Góp

Chúng tôi rất hoan nghênh mọi đóng góp! Đây là cách bạn có thể giúp:

1. Fork repository này
2. Tạo nhánh tính năng mới
3. Commit các thay đổi của bạn
4. Push lên nhánh của bạn
5. Tạo Pull Request

## 📝 Giấy Phép

Dự án này được cấp phép theo Giấy phép MIT - xem file LICENSE để biết thêm chi tiết.

## 👥 Liên Hệ

- Người phát triển: [@smlnobita](https://t.me/smlnobita) trên Telegram
- Báo lỗi: Sử dụng GitHub issue tracker

---

Được tạo với ❤️ bởi đội ngũ BéHoà-4o