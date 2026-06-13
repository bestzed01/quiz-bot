#!/usr/bin/env python3
"""
Uzbek quiz bot — Pedagogika va Psixologiya
Telegram Mini App version
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# The URL where webapp.html is hosted (set via env var)
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://your-app.railway.app")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(
        "🎓 Quizni boshlash",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    await update.message.reply_text(
        "👋 <b>Pedagogika va Psixologiya Quiz</b>\n\n"
        "📚 <b>917 ta savol</b> — barcha fanlar bo'yicha\n\n"
        "Pastdagi tugmani bosib quizni oching:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

async def post_init(app: Application):
    # Set menu button to open the web app directly
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="📝 Quiz", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    # Register commands
    await app.bot.set_my_commands([
        ("start", "Botni ishga tushirish"),
        ("quiz", "Quizni ochish"),
        ("help", "Yordam"),
    ])
    logger.info(f"Bot ready. WebApp URL: {WEBAPP_URL}")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 <b>Qo'llanma</b>\n\n"
        "• /start yoki /quiz — quizni ochish\n"
        "• Pastdagi <b>📝 Quiz</b> tugmasi — tezkor kirish\n\n"
        "Quiz ichida:\n"
        "• Javobni tanlang → ✅ yoki ❌ ko'rsatiladi\n"
        "• <b>Keyingi savol ➜</b> bilan davom eting\n"
        "• Oxirida natijangizni ko'rasiz",
        parse_mode="HTML"
    )

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN not set!")

    app = Application.builder().token(token).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("help", help_cmd))

    logger.info("Bot polling...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
