from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os
import logging
from dotenv import load_dotenv
from agent import Agent

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Hello!
I am an AI-powered YouTube Summarizer Telegram Bot that generates concise video summaries.
Check out the code on GitHub: https://github.com/Chirag-Juneja/yt_summarize_en_bot"""
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Send me a youtube link and i will summarize the video for you."""
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """This bot is made by Chirag Juneja.
Connect with me:
Github: https://github.com/Chirag-Juneja
LinkedIn: https://www.linkedin.com/in/chirag-juneja-45bab4a7/
"""
    )


async def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    logger.info(text)
    if message_type == "group":
        pass
    else:
        response = agent(text)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    load_dotenv()

    TOKEN = os.getenv("TOKEN")
    POLLING = int(os.getenv("POLLING"))

    model_name = os.getenv("MODEL")
    agent = Agent(model_name=model_name)

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Entity("url") | filters.Entity("text_link"),
            url_handler,
        )
    )
    app.add_error_handler(error)
    logger.info(f"Starting telegram bot with {POLLING}sec polling")
    app.run_polling(poll_interval=POLLING)
