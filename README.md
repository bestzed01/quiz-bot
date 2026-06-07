# Pedagogika va Psixologiya Quiz Bot

**971 ta savol** (barcha fayllardan to'plangan):
- Pedagogik mahorat (xlsx)
- Pedagogika nazariyasi va tarixi (xlsx)
- TFO'M DAK test savollari (xlsx)
- Sotsial psixologiya (docx)
- Psixologiya tarixi — 200 test (doc)

## Ishga tushirish

### 1. Bot yaratish
[@BotFather](https://t.me/BotFather) ga yozing → `/newbot` → token oling

### 2. Fayllarni serverga joylashtiring
```
bot.py
questions.json
```

### 3. Kutubxonani o'rnating
```bash
pip install python-telegram-bot
```

### 4. Botni ishga tushiring
```bash
BOT_TOKEN="sizning_tokeningiz" python3 bot.py
```

Yoki `.env` faylida saqlang:
```bash
export BOT_TOKEN="sizning_tokeningiz"
python3 bot.py
```

## Buyruqlar
- `/start` — Quiz boshlash
- `/stop` — To'xtatish va natijani ko'rsatish
- `/score` — Joriy natijani ko'rish

## Qanday ishlaydi
Har safar tasodifiy savol beriladi, 4 ta variant (A/B/C/D).  
Javob bosgandan so'ng:
- ✅ — to'g'ri
- ❌ — noto'g'ri (to'g'ri javob ko'rsatiladi)
