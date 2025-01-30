# 🤖 BéHoà-4o Telegram Bot

**BéHoà-4o** là chatbot Telegram thông minh sử dụng **GPT-4o**, cung cấp khả năng trò chuyện tự nhiên cùng nhiều tính năng tiện ích:

- 📈 **Tra cứu giá vàng**, tỷ giá ngoại tệ, giá tiền ảo theo thời gian thực.
- ⏰ **Xem thời gian hiện tại** (Dương lịch & Âm lịch).
- 📃 **Quản lý và lưu trữ lịch sử chat**.
- 🖼️ **Hỗ trợ tạo ảnh**.
- 🌐 **Hỗ trợ đa ngôn ngữ**.

---

## 🚀 Tính năng chính

✔️ **Chat AI thông minh** với GPT-4o  
✔️ **Tra cứu giá vàng** theo khu vực (SJC & PNJ)  
✔️ **Xem tỷ giá ngoại tệ** từ Vietcombank  
✔️ **Theo dõi giá tiền ảo** từ Binance  
✔️ **Hệ thống giới hạn tin nhắn** theo giai đoạn  
✔️ **Hỗ trợ lịch sử chat** và quản lý tin nhắn  
✔️ **Hỗ trợ tạo ảnh**  
✔️ **Hỗ trợ đa ngôn ngữ**  

---

## 🛠 Yêu cầu hệ thống

- **Python** 3.10+
- **pip** (Python package manager)

---

## 🔧 Hướng dẫn cài đặt

### 1️⃣ Clone repository  
```bash
git clone https://github.com/SMLnobita/behoa-telegram-bot.git
cd behoa-telegram-bot
```

### 2️⃣ Cài đặt thư viện cần thiết  
```bash
pip install -r requirements.txt
```

### 3️⃣ Cài đặt biến môi trường  
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
| `/time`    | Xem thời gian hiện tại (Âm lịch & Dương lịch) |
| `/info`    | Xem thông tin cá nhân |
| `/vang`    | Xem giá vàng SJC & PNJ |
| `/ngoaite` | Xem tỷ giá ngoại tệ |
| `/image <description>` | Tạo hình ảnh theo mô tả |
| `/tienao`  | Xem giá tiền ảo từ Binance |

---

## ⚙️ Hệ thống giới hạn tin nhắn

🔹 **Giai đoạn 1 (Initial)**  
   - Giới hạn: **10 tin nhắn**  
   - Mở rộng bằng nút "Tiếp tục nhắn"  

🔹 **Giai đoạn 2 (Extended)**  
   - Giới hạn: **20 tin nhắn**  
   - Yêu cầu nhập key để tiếp tục  

🔹 **Giai đoạn 3 (Key Used)**  
   - Giới hạn: **35 tin nhắn**  
   - Giai đoạn cuối cùng  

---

## 🚀 Khởi chạy bot
```bash
python main.py
```

---

## 💡 Đóng góp
Bạn có thể mở issue hoặc gửi pull request để cải thiện dự án. Nếu có thay đổi lớn, vui lòng mở issue trước để thảo luận.

## 📞 Liên hệ
- Telegram: [@smlnobita](https://t.me/smlnobita)

## 📜 Giấy phép
Dự án này được cấp phép theo MIT License. Xem thêm tại file LICENSE.

## 🙌 Cảm ơn
Xin gửi lời cảm ơn đến:  
- 💰 **Binance, Vietcombank, và PNJ** vì các dịch vụ dữ liệu 
---

⚡ *Hãy đóng góp và cùng nhau phát triển dự án!* 🚀 

