# ============================================================
# Telegram Bot for DI GenAI Content Pipeline
# Compatible python-telegram-bot v21.5
# CLEAN event loop, no asyncio.run issues
# ============================================================

import os
import sys
import json
import datetime
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# -----------------------------------------------------------
# Load .env safely
# -----------------------------------------------------------
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("ERROR: TELEGRAM_BOT_TOKEN not found in .env")

# -----------------------------------------------------------
# Fix Python path for imports
# -----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from pipeline import ContentPipeline  # now works cleanly


# -----------------------------------------------------------
# Global pipeline (ONLY ONE INSTANCE)
# -----------------------------------------------------------
pipeline = ContentPipeline(use_api=True)


# -----------------------------------------------------------
# HELPER: Back to menu button
# -----------------------------------------------------------
def back_to_menu_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back to menu", callback_data="back_to_menu")]
    ])


# -----------------------------------------------------------
# Helper: Send long messages without Telegram cutoff
# -----------------------------------------------------------
async def send_long_message(update: Update, text: str):
    MAX = 4000

    if update.message:
        send_func = update.message.reply_text
    else:
        send_func = update.callback_query.message.reply_text

    # If short enough, send once
    if len(text) <= MAX:
        await send_func(text, parse_mode="Markdown")
        await send_func("⬅️ Back to menu", reply_markup=back_to_menu_button(), parse_mode="Markdown")
        return

    # Split long messages
    parts = text.split("\n")
    chunk = ""

    for line in parts:
        if len(chunk) + len(line) + 1 > MAX:
            await send_func(chunk, parse_mode="Markdown")
            chunk = line + "\n"
        else:
            chunk += line + "\n"

    if chunk.strip():
        await send_func(chunk, parse_mode="Markdown")

    # Send Back to Menu button after the last chunk
    await send_func("⬅️ Back to menu", reply_markup=back_to_menu_button(), parse_mode="Markdown")


# -----------------------------------------------------------
# Format results nicely for Telegram
# -----------------------------------------------------------
def format_results(results):
    out = "📄 *Last results:*\n\n"
    for r in results:
        snippet = r["generated_text"][:3000]
        if len(r["generated_text"]) > 3000:
            snippet += "..."

        out += f"• *{r['prompt']}*\n→ {snippet}\n"

        if r["flagged"]:
            out += f"⚠️ Flagged: {', '.join(r['flagged_words'])}\n"

        out += "\n"
    return out


# -----------------------------------------------------------
# Menu keyboard
# -----------------------------------------------------------
def get_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣ Run default pipeline", callback_data="menu_1")],
        [InlineKeyboardButton("2️⃣ Custom prompt", callback_data="menu_2")],
        [InlineKeyboardButton("3️⃣ Run batch CSV", callback_data="menu_3")],
        [InlineKeyboardButton("4️⃣ Last results", callback_data="menu_4")],
    ])


# -----------------------------------------------------------
# /start command
# -----------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *DI Content Pipeline Bot Ready!* 🔥\n"
        "Choose an option:",
        reply_markup=get_menu_keyboard(),
        parse_mode="Markdown"
    )


# -----------------------------------------------------------
# BACK TO MENU HANDLER
# -----------------------------------------------------------
async def back_to_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📋 *Main Menu:*",
        reply_markup=get_menu_keyboard(),
        parse_mode="Markdown"
    )


# -----------------------------------------------------------
# Handle menu button clicks
# -----------------------------------------------------------
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    choice = query.data
    await query.answer()

    if choice == "back_to_menu":
        return await back_to_menu_handler(update, context)

    # 1) default pipeline
    if choice == "menu_1":
        results = pipeline.run()
        txt = format_results(results)
        await send_long_message(update, txt)
        return

    # 2) custom prompt
    if choice == "menu_2":
        await query.edit_message_text("✍️ Send your prompt:")
        context.user_data["awaiting_prompt"] = True
        return

    # 3) batch CSV
    if choice == "menu_3":
        results = pipeline.run_batch_csv()
        txt = format_results(results)
        await send_long_message(update, txt)
        return

    # 4) last results
    if choice == "menu_4":
        results = pipeline.get_last_results()
        if not results:
            await query.edit_message_text("❌ No previous results found.")
            return

        txt = format_results(results)
        await send_long_message(update, txt)
        return


# -----------------------------------------------------------
# Handle custom prompt text entry
# -----------------------------------------------------------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_prompt"):
        prompt = update.message.text
        context.user_data["awaiting_prompt"] = False

        results = pipeline.process_single(prompt)
        txt = format_results(results)
        await send_long_message(update, txt)
        return

    # Otherwise redirect to menu
    await update.message.reply_text(
        "Use the menu below:",
        reply_markup=get_menu_keyboard()
    )


# -----------------------------------------------------------
# Main launcher — NO asyncio.run()
# -----------------------------------------------------------
def main():
    print("🤖 Telegram bot running (clean event loop)…")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(back_to_menu_handler, pattern="back_to_menu"))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
