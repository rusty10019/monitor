# 📱 SHEIN Wishlist Monitor

Monitor your SHEIN wishlist and get instant Telegram notifications when products come back in stock!

---

## 🚀 Quick Setup

### 1. Clone Repository

```bash
git clone https://github.com/rusty10019/monitor.git
cd monitor
```

### 2. Create Your Own Bot

1. Open Telegram
2. Search: **@BotFather**
3. Send: `/newbot`
4. Choose a name (e.g., "My SHEIN Monitor")
5. Choose a username (e.g., "myshein_bot")
6. Copy the bot token

### 3. Configure Bot Token

```bash
nano user_monitor_simple.py
```

Find this line:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

Replace with your token:
```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

Save: `Ctrl+X`, `Y`, `Enter`

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

### 5. Get Your SHEIN Cookies

1. Open https://www.sheinindia.in/ in browser
2. Login to your account
3. Press `F12` → Go to **Network** tab
4. Refresh page (`F5`)
5. Click any request → Find **Cookie** header
6. Copy the entire cookie string

### 6. Create cookies.txt

```bash
nano cookies.txt
# Paste your cookies
# Save: Ctrl+X, Y, Enter
```

### 7. Get Your Chat ID

1. Open Telegram
2. Search for YOUR bot (the one you created)
3. Send: `/start`
4. Send any message
5. Go to: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
6. Find your Chat ID in the response

### 8. Run Script

```bash
python3 user_monitor_simple.py
```

Enter your Chat ID when prompted.

---

## 🔔 Notifications

You'll receive instant Telegram alerts when products come back in stock:

```
🔔 IN-STOCK ALERT!
━━━━━━━━━━━━━━━━
📦 Product: Women's Dress
📏 Size: M
💰 Price: Rs.599
━━━━━━━━━━━━━━━━
🛒 [OPEN PRODUCT]
```

---

## 🖥️ Run on Android (Termux)

```bash
pkg install python git
git clone https://github.com/rusty10019/monitor.git
cd monitor
pip install -r requirements.txt
python3 user_monitor_simple.py
```

### Keep Running in Background

```bash
# Option 1: tmux
pkg install tmux
tmux new -s monitor
python3 user_monitor_simple.py
# Detach: Ctrl+B, then D

# Option 2: nohup
nohup python3 user_monitor_simple.py &
```

---

## 📋 Requirements

- Python 3.7+
- Internet connection
- SHEIN account with wishlist
- Telegram account

## 💻 Supported Platforms

- ✅ Linux (Termux/Android)
- ✅ Windows
- ✅ Mac

---

## ❓ Troubleshooting

### "cookies.txt not found"
Create the file: `nano cookies.txt` and paste your cookies

### "Invalid cookies"
Get fresh cookies from SHEIN (they expire)

### "Failed to send message"
Check your Chat ID is correct (numbers only)

### Script stops when terminal closes
Run in background: `nohup python3 user_monitor_simple.py &`

---

## 🔒 Privacy

- ✅ Runs on YOUR device
- ✅ Uses YOUR cookies
- ✅ Uses YOUR IP
- ✅ Open source code

---

## 👤 Credits

**Created by:** @rusty_whoo  
**Channels:** @rusty_whoo & @Looters_01

---

## 📞 Support

Need help? Ask in Telegram:
- @rusty_whoo
- @Looters_01

---

**Happy shopping!** 🛍️
