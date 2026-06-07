#!/usr/bin/env python3
"""
Uzbek quiz bot — Pedagogika va Psixologiya
"""

import json
import logging
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Load questions
with open(os.path.join(os.path.dirname(__file__), "questions.json"), encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

TOTAL_Q = len(ALL_QUESTIONS)

ASKING = 1


def build_question(user_data: dict) -> tuple[str, InlineKeyboardMarkup, str]:
    """Pick a random question and return text, keyboard, correct answer."""
    q = random.choice(ALL_QUESTIONS)
    question_text = q["q"]
    correct = q["correct"]
    
    options = [correct] + q["wrong"][:3]   # up to 4 choices
    random.shuffle(options)
    
    # Store correct answer
    user_data["correct"] = correct
    user_data["options"] = options
    
    # Build inline keyboard (one button per row)
    keyboard = []
    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(options):
        label = f"{letters[i]}. {opt}"
        # callback_data carries the letter so we know which was picked
        keyboard.append([InlineKeyboardButton(label, callback_data=f"ans:{letters[i]}")])
    
    user_data["letter_map"] = {letters[i]: options[i] for i in range(len(options))}
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return question_text, reply_markup, correct


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command — show welcome and first question."""
    context.user_data.clear()
    context.user_data["score"] = 0
    context.user_data["total"] = 0
    
    await update.message.reply_text(
        f"🎓 <b>Pedagogika va Psixologiya Quiz Bot</b>\n\n"
        f"Umumiy savollar soni: <b>{TOTAL_Q}</b> ta\n\n"
        f"Har safar tasodifiy savol beriladi. "
        f"To'g'ri javobga ✅, noto'g'riga ❌ qo'yiladi.\n\n"
        f"Boshlaylik! /stop — to'xtatish uchun.",
        parse_mode="HTML",
    )
    await send_question(update.message.chat_id, context)
    return ASKING


async def send_question(chat_id, context: ContextTypes.DEFAULT_TYPE):
    """Send a new question to the given chat."""
    question_text, markup, _ = build_question(context.user_data)
    score = context.user_data.get("score", 0)
    total = context.user_data.get("total", 0)
    
    header = f"📊 <b>{score}/{total}</b> · Savol #{total + 1}\n\n"
    await context.bot.send_message(
        chat_id=chat_id,
        text=header + f"❓ {question_text}",
        reply_markup=markup,
        parse_mode="HTML",
    )


async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle answer button press."""
    query = update.callback_query
    await query.answer()
    
    data = query.data  # "ans:A"
    chosen_letter = data.split(":")[1]
    
    letter_map: dict = context.user_data.get("letter_map", {})
    correct: str = context.user_data.get("correct", "")
    chosen_text = letter_map.get(chosen_letter, "")
    
    is_correct = (chosen_text == correct)
    
    context.user_data["total"] = context.user_data.get("total", 0) + 1
    if is_correct:
        context.user_data["score"] = context.user_data.get("score", 0) + 1
    
    score = context.user_data["score"]
    total = context.user_data["total"]
    
    # Build result keyboard — show all options with marks
    letters = ["A", "B", "C", "D"]
    keyboard = []
    for letter in letters:
        text = letter_map.get(letter)
        if text is None:
            continue
        if text == correct:
            label = f"✅ {letter}. {text}"
        elif text == chosen_text and not is_correct:
            label = f"❌ {letter}. {text}"
        else:
            label = f"   {letter}. {text}"
        keyboard.append([InlineKeyboardButton(label, callback_data="done")])
    
    keyboard.append([InlineKeyboardButton("➡️ Keyingi savol", callback_data="next")])
    
    result_icon = "✅ To'g'ri!" if is_correct else f"❌ Noto'g'ri!\n📖 To'g'ri javob: <b>{correct}</b>"
    
    await query.edit_message_text(
        text=(
            f"📊 <b>{score}/{total}</b>\n\n"
            f"❓ {context.user_data.get('options', [''])[0] if False else query.message.text.split('❓ ', 1)[-1]}\n\n"
            f"{result_icon}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )
    return ASKING


async def next_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle 'Next question' button."""
    query = update.callback_query
    await query.answer()
    await send_question(query.message.chat_id, context)
    return ASKING


async def done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ignore taps on result buttons."""
    await update.callback_query.answer()
    return ASKING


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stop command — show final score."""
    score = context.user_data.get("score", 0)
    total = context.user_data.get("total", 0)
    pct = round(score / total * 100) if total else 0
    
    if pct >= 90:
        emoji = "🏆"
    elif pct >= 70:
        emoji = "🎓"
    elif pct >= 50:
        emoji = "📚"
    else:
        emoji = "💪"
    
    await update.message.reply_text(
        f"{emoji} <b>Yakuniy natija</b>\n\n"
        f"To'g'ri javoblar: <b>{score}</b> / {total}\n"
        f"Foiz: <b>{pct}%</b>\n\n"
        f"Yana boshlash uchun /start",
        parse_mode="HTML",
    )
    context.user_data.clear()
    return ConversationHandler.END


async def score_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show current score."""
    score = context.user_data.get("score", 0)
    total = context.user_data.get("total", 0)
    pct = round(score / total * 100) if total else 0
    await update.message.reply_text(
        f"📊 Hozirgi natija: <b>{score}/{total}</b> ({pct}%)\n"
        f"Jami savollar bazada: <b>{TOTAL_Q}</b> ta",
        parse_mode="HTML",
    )


def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan!")
    
    app = Application.builder().token(token).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASKING: [
                CallbackQueryHandler(answer_callback, pattern="^ans:"),
                CallbackQueryHandler(next_callback, pattern="^next$"),
                CallbackQueryHandler(done_callback, pattern="^done$"),
            ]
        },
        fallbacks=[
            CommandHandler("stop", stop),
            CommandHandler("start", start),
        ],
        per_user=True,
        per_chat=True,
    )
    
    app.add_handler(conv)
    app.add_handler(CommandHandler("score", score_cmd))
    
    logger.info(f"Bot ishga tushdi. Jami {TOTAL_Q} ta savol yuklandi.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
