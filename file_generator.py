import os
from time import sleep

import pytube.exceptions as exceptions
import requests
import telebot
from dotenv import load_dotenv
from pytube import YouTube, Stream
from pytube.helpers import safe_filename

from message import Message

load_dotenv()


class FileGenerator:

    """
    A class for performing all the necessary file uploading and deleting processes. The basic idea is to use pytube to
    download an audio file from a link and send it to the user. At the end, it deletes the downloaded file from the
    system and deletes all unnecessary messages, such as links and bot messages about the download process.
    """

    bot = telebot.TeleBot(os.getenv('BOT_API_KEY'))

    @classmethod
    def delete_unnecessary_messages(cls, chat_id: int, message_ids: list):
        sleep(5)
        for message_id in message_ids:
            cls.bot.delete_message(chat_id=chat_id, message_id=message_id)

    @classmethod
    def delete_unnecessary_file_and_messages(
            cls, file_path: str, chat_id: int, message_ids: list, max_retries: int = 5
    ):
        if max_retries > 0:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                cls.delete_unnecessary_messages(chat_id=chat_id, message_ids=message_ids)
            except PermissionError:
                sleep(5)
                cls.delete_unnecessary_file_and_messages(
                    file_path=file_path, chat_id=chat_id, message_ids=message_ids, max_retries=max_retries - 1
                )

    @classmethod
    def generate_and_send_file(cls, chat_id: int, audio_link: str, link_message_id: str):
        try:
            downloading_message_obj = cls.bot.send_message(chat_id, text=Message.downloading_file(), parse_mode='html')
            downloading_message_obj_id = downloading_message_obj.message_id
            cls.bot.send_chat_action(chat_id, 'record_video')
            stream_obj = YouTube(audio_link)
            availability = stream_obj.check_availability()
            if not availability:
                file_obj = stream_obj.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').first()
                if file_obj.filesize < 50000000:
                    file_path = cls.get_or_create_file(file_obj)
                    downloaded_message_obj_id = cls.send_audio_file(
                        file_path=file_path, chat_id=chat_id, downloading_message_obj_id=downloading_message_obj_id
                    )
                    cls.delete_unnecessary_file_and_messages(
                        file_path=file_path, chat_id=chat_id, message_ids=[link_message_id, downloaded_message_obj_id]
                    )
                else:
                    cls.bot.send_message(chat_id, text=Message.too_large_file())
            else:
                cls.bot.send_message(chat_id, text=Message.unavailable_link(availability))
        except (exceptions.VideoUnavailable, exceptions.RegexMatchError):
            cls.bot.send_message(chat_id, text=Message.unworked_link())

    @classmethod
    def get_or_create_file(cls, file_obj: Stream) -> str:
        file_name = safe_filename(file_obj.title)
        if not os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + '/files/' + file_name):
            file_path = file_obj.download(output_path='files', filename=file_name)
        else:
            file_path = str(os.path.dirname(os.path.abspath(__file__)) + '/files/' + file_name)
        return file_path

    @classmethod
    def send_audio_file(cls, file_path: str, chat_id: int, downloading_message_obj_id: int) -> int:
        downloaded_message = cls.bot.edit_message_text(
            chat_id=chat_id,
            message_id=downloading_message_obj_id,
            text=Message.success_downloaded(),
            parse_mode='HTML',
        )
        with open(file_path, 'rb') as audio_file:
            cls.bot.send_chat_action(chat_id, 'record_video')
            try:
                cls.bot.send_audio(chat_id, audio=audio_file, timeout=300)
                finished_message = cls.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=downloaded_message.message_id,
                    text=Message.success_sent(),
                )
            except requests.exceptions.SSLError:
                finished_message = cls.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=downloaded_message.message_id,
                    text=Message.sending_audio_error(),
                )
        return finished_message.message_id
