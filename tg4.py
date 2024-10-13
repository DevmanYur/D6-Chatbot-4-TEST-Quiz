import os
from datetime import datetime

import requests
import telegram
from dotenv import load_dotenv
import logging
import time


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]

    update.message.reply_text(
        'Hi!',
        reply_markup=ReplyKeyboardMarkup(custom_keyboard,
                                         one_time_keyboard=True,
                                         input_field_placeholder='Boy or Girl?'
                                         ),
    )

    return GENDER

def main():
    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']
    tg_bot = telegram.Bot(token=telegram_token)
    chat_id = tg_bot.get_updates()[0].message.from_user.id


    #
    # while True:
    #     custom_keyboard = [['Новый вопрос', 'Сдаться'],
    #                        ['Мой счёт']]




if __name__ == '__main__':
    main()