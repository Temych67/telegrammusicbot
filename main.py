import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Help you!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('BOT_API_KEY')).build()

    start_handler = CommandHandler('start', start_command)
    help_handler = CommandHandler('help', help_command)
    application.add_handler(start_handler)
    application.add_handler(help_handler)

    application.run_polling()
