# 🤖 BéHoà-4o Telegram Bot

BéHoà-4o là một chatbot Telegram thông minh, được phát triển bằng Python, tích hợp **GPT-4o** để hỗ trợ trò chuyện và nhiều tính năng hữu ích khác.

## 🚀 Tính năng nổi bật

- 💬 **Chat thông minh** với GPT-4o
- 🎨 **Tạo hình ảnh** với DALL·E 3
- 💰 **Tra cứu giá vàng** (SJC & PNJ)
- 💱 **Xem tỷ giá ngoại tệ** (Vietcombank)
- 🪙 **Theo dõi giá tiền ảo** (Binance)
- ⏰ **Xem thời gian** (Dương lịch & Âm lịch)
- 🌤️ **Xem thời tiết** tại nhiều thành phố
- 🔄 **Quản lý tin nhắn** theo giai đoạn

## 🛠 Yêu cầu hệ thống

- **Python** 3.8+
- **pip** (Python package installer)
- **Telegram Bot Token**
- **OpenAI API Key**

## 📦 Cài đặt

### 1️⃣ Clone repository
```bash
git clone https://github.com/SMLnobita/behoa-telegram-bot.git
cd behoa-telegram-bot
```

### 2️⃣ Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Cấu hình biến môi trường
Tạo tệp `.env` và thêm thông tin:
```ini
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## 🚀 Khởi chạy bot
```bash
python main.py
```

## 📂 Cấu trúc dự án
```
behoa-telegram-bot/
├── config.py             # Cấu hình và biến môi trường
├── enums.py              # Định nghĩa các enum
├── keywords.py           # Danh sách từ khóa
├── main.py               # Điểm khởi động ứng dụng
├── models.py             # Định nghĩa các model
│
├── handlers/             # Xử lý tin nhắn
│   ├── callback_handler.py
│   ├── chat_handler.py
│   ├── message_commands.py
│
├── managers/             # Quản lý trạng thái
│   └── user_manager.py
│
├── trackers/             # Theo dõi dữ liệu
│   ├── crypto_tracker.py
│   ├── currency_tracker.py
│   ├── gold_tracker.py
│   └── weather_tracker.py
│
└── utils/               # Tiện ích
    ├── message_handler.py
    └── openai_handler.py
```

## 📝 Danh sách lệnh bot

| Lệnh | Mô tả |
|------------|-------------------------------|
| `/start` | Khởi động bot và xóa lịch sử chat |
| `/help` | Hướng dẫn sử dụng bot |
| `/clear` | Xóa lịch sử chat |
| `/time` | Xem thời gian hiện tại |
| `/info` | Xem thông tin người dùng |
| `/thoitiet` | Xem dự báo thời tiết |
| `/image <mô tả>` | Tạo hình ảnh từ mô tả |
| `/vang` | Xem giá vàng (SJC & PNJ) |
| `/ngoaite` | Xem tỷ giá ngoại tệ (Vietcombank) |
| `/tienao` | Xem giá tiền ảo (Binance) |

## ⏳ Hệ thống giới hạn tin nhắn

BéHoà-4o có cơ chế giới hạn tin nhắn theo các giai đoạn:

| Giai đoạn | Số tin nhắn | Điều kiện |
|-----------|------------|------------|
| **1** | 5 tin | Mặc định ban đầu |
| **2** | 10 tin | Sau khi nhấn "Tiếp tục nhắn" |
| **3** | 15 tin | Sau khi nhập key |

⏳ **Thời gian chờ giữa các tin nhắn:** 3 giây

## 🤖 Tính năng chat thông minh

- 💬 Sử dụng GPT-4o cho trò chuyện thông minh
- 🎯 Hiểu và trả lời được nhiều ngôn ngữ
- 📚 Lưu trữ lịch sử chat để duy trì ngữ cảnh
- 🔄 Tự động xóa lịch sử khi restart hoặc clear
- ⚡ Phản hồi nhanh với thời gian chờ tối thiểu

## 🌟 Tính năng đặc biệt

### 🎨 Tạo hình ảnh với DALL·E 3
- Sử dụng công nghệ DALL·E 3 mới nhất
- Hỗ trợ tạo ảnh với độ phân giải cao
- Có thể tạo ảnh từ mô tả chi tiết

### 💰 Theo dõi giá cả
- Cập nhật giá vàng SJC và PNJ theo thời gian thực
- Theo dõi tỷ giá ngoại tệ từ Vietcombank
- Xem giá tiền ảo trên Binance

### ⏰ Thời gian và thời tiết
- Hiển thị thời gian theo cả dương lịch và âm lịch
- Cập nhật thời tiết cho nhiều thành phố
- Thông tin về chất lượng không khí

## 🛠 Hướng dẫn phát triển

### Thêm tính năng mới
1. **Tạo handler mới** trong thư mục `handlers/`
2. **Đăng ký handler** trong `main.py`
3. **Cập nhật tài liệu** để người dùng biết cách sử dụng

### Quản lý dependencies
- Sử dụng `requirements.txt` để quản lý thư viện
- Kiểm tra và cập nhật phiên bản thường xuyên
- Đảm bảo tương thích giữa các thư viện

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📜 Giấy phép

BéHoà-4o được phát hành theo giấy phép MIT.

## 👤 Tác giả

- **[@smlnobita](https://t.me/smlnobita)** (Telegram)

## 📞 Liên hệ

Nếu có bất kỳ câu hỏi hoặc góp ý, hãy liên hệ qua:
- 💬 **Telegram:** [@smlnobita](https://t.me/smlnobita)

🔥 **Cảm ơn bạn đã sử dụng BéHoà-4o! Chúc bạn có trải nghiệm tuyệt vời!** 🎉