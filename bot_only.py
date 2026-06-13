#!/usr/bin/env python3
import logging, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButtonWebApp, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBAPP_URL = os.environ.get("WEBAPP_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎓 Quizni boshlash", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(
        "👋 <b>Pedagogika va Psixologiya Quiz</b>\n\n"
        "📚 <b>917 ta savol</b> — barcha fanlar bo'yicha\n\n"
        "Pastdagi tugmani bosib quizni oching:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )

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
        parse_mode="HTML",
    )

async def post_init(app: Application):
    await app.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="📝 Quiz", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await app.bot.set_my_commands([
        ("start", "Botni ishga tushirish"),
        ("quiz", "Quizni ochish"),
        ("help", "Yordam"),
    ])
    logger.info(f"Bot ready. WebApp: {WEBAPP_URL}")

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set!")
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("help", help_cmd))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
