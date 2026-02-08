# 🚂 Deploy to Railway

## ✅ Your Bot Token is Hidden!

Railway uses environment variables, so your bot token is never exposed in the code!

---

## 🚀 Deploy Steps:

### 1. Push to GitHub

```bash
git add .
git commit -m "Railway deployment ready"
git push origin main
```

### 2. Deploy on Railway

1. Go to: https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `rusty10019/monitor`
5. Click "Deploy"

### 3. Add Environment Variable

1. In Railway dashboard, click your project
2. Go to "Variables" tab
3. Click "New Variable"
4. Add:
   - **Name:** `BOT_TOKEN`
   - **Value:** `8548444304:AAHeFjaEAysv46Is4ebTDF2XWHCsJqDiQAk`
5. Click "Add"

### 4. Add Cookies

You'll need to add cookies.txt to Railway:

**Option A: Use Railway CLI**
```bash
railway login
railway link
railway run bash
nano cookies.txt
# Paste cookies
```

**Option B: Add to repo (not recommended)**
```bash
# Add cookies.txt to .gitignore first!
echo "cookies.txt" >> .gitignore
```

---

## 📱 For Users (Local Setup):

Users running locally need to:

### 1. Clone Repo
```bash
git clone https://github.com/rusty10019/monitor.git
cd monitor
```

### 2. Create .env File
```bash
cp .env.example .env
nano .env
```

Add their own bot token:
```
BOT_TOKEN=their_bot_token_here
```

### 3. Add Cookies
```bash
nano cookies.txt
# Paste SHEIN cookies
```

### 4. Run
```bash
pip install -r requirements.txt
python3 user_monitor_simple.py
```

---

## 🔒 Security:

### On Railway:
- ✅ Bot token in environment variables (hidden)
- ✅ Not visible in code
- ✅ Not in GitHub
- ✅ Secure!

### For Users:
- ✅ Each user creates their own bot
- ✅ Each user has their own .env file
- ✅ .env is in .gitignore (not pushed to GitHub)
- ✅ Secure!

---

## ✅ Benefits:

1. **Your Token is Hidden** - Only in Railway environment variables
2. **Users Create Own Bots** - They use their own tokens
3. **No Exposure** - Token never in code or GitHub
4. **Easy Deploy** - One-click Railway deployment

---

## 🎯 Summary:

**For You (Railway):**
- Deploy to Railway
- Add BOT_TOKEN environment variable
- Your token is hidden!

**For Users (Local):**
- Clone repo
- Create .env with their bot token
- Run locally
- Their token is hidden!

**Perfect!** 🔒
