import logging
import os
from functools import partial
import random

import redis
from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger(__name__)

def get_units():
   with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
       file_contents = my_file.read()
       file_contents_split = file_contents.split('\n\n\n')
       units = []
       for questions_and_answers in  file_contents_split:
           question_and_answer = questions_and_answers.split('\n\n')
           question_fields, answer_fields, source_fields, author_fields = question_and_answer
           question_field, question =  question_fields.split('\n')
           answer_field, answer = answer_fields.split('\n')
           source_field, source = source_fields.split('\n')
           author_field, author = author_fields.split('\n')
           unit_dict = {'Вопрос': question,
                            'Ответ': answer,
                            'Источник': source,
                            'Автор': author}
           units.append(unit_dict)
       return units


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        text="Custom Keyboard Test",
        reply_markup=reply_markup)


def get_question(units_dict, redis_object,  update: Update, context: CallbackContext):
    unit = random.choice(units_dict)
    print('юнит', unit)
    update.message.reply_text('Сейчас отправлю новый вопрос!__')
    update.message.reply_text(unit['Вопрос'])
    chat_id = update.message.chat_id

    redis_object.mset(unit)
    redis_object.set('chat_id', chat_id)
    update.message.reply_text(redis_object.get('Вопрос'))
    update.message.reply_text(redis_object.get('Ответ'))
    update.message.reply_text(redis_object.get('chat_id'))


def give_in(update: Update, context: CallbackContext):
    update.message.reply_text('Точно сдаться?')

def get_my_account(update: Update, context: CallbackContext):
    update.message.reply_text('Сделал запрос на Мой счёт.')


def send_answer(redis_object, update: Update, context: CallbackContext):
    answer = redis_object.get('Ответ')
    if update.message.text == answer:
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    else:
        update.message.reply_text(f'Неправильно… Верный ответ {answer}')


def start_tg_bot(telegram_token, redis_object, units):
    get_new_question = partial(get_question, units, redis_object)
    send_new_answer = partial(send_answer, redis_object)

    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text('Новый вопрос'), get_new_question))
    dispatcher.add_handler(MessageHandler(Filters.text('Сдаться'), give_in))
    dispatcher.add_handler(MessageHandler(Filters.text('Мой счёт'), get_my_account))
    dispatcher.add_handler(MessageHandler(Filters.text, send_new_answer))
    updater.start_polling()
    updater.idle()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    redis_object = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    units = get_units()

    start_tg_bot(telegram_token, redis_object, units)

if __name__ == '__main__':
    main()