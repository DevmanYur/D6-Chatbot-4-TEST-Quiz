import os
from datetime import datetime

import requests
import telegram
from dotenv import load_dotenv
import logging
import time


logger = logging.getLogger('Logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_notification(tg_bot, chat_id):
    text = 'https://dvmn.org/api/long_polling/'
    tg_bot.send_message(chat_id=chat_id, text=text)


def get_notification2(tg_bot, chat_id):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    tg_bot.send_message(chat_id=chat_id,
                     text="Custom Keyboard Test",
                     reply_markup=reply_markup)

def get_notification3(tg_bot, chat_id):
    question = chat_id.message.text
    chat_id = chat_id.message.chat_id
    text = 'https://dvmn.org/api/long_polling/'
    tg_bot.send_message(chat_id=chat_id, text=question)

def main():
    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']
    tg_bot = telegram.Bot(token=telegram_token)
    chat_id = tg_bot.get_updates()[0].message.from_user.id

    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tg_bot, chat_id))

    while True:
        custom_keyboard = [['Новый вопрос', 'Сдаться'],
                           ['Мой счёт']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        # tg_bot.send_message(chat_id=chat_id,
        #                     text="Custom Keyboard Test",
        #                     reply_markup=reply_markup)






if __name__ == '__main__':
    main()