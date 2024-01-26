import os

import telebot
from dotenv import load_dotenv

from file_generator import FileGenerator
from message import Message

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_API_KEY'))


@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.from_user
    bot.send_message(message.chat.id, text=Message.start(user.first_name, user.last_name))


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, text=Message.help())


@bot.message_handler(content_types=['text'])
def processing_link_command(message):
    audio_link = message.text
    chat_id = message.chat.id
    if not audio_link.startswith('https://'):
        bot.send_chat_action(chat_id, 'typing')
        bot.send_message(message.chat.id, text=Message.inappropriate_text())
    else:
        FileGenerator.generate_and_send_file(chat_id=chat_id, audio_link=audio_link, link_message_id=message.message_id)


bot.polling(none_stop=True)
