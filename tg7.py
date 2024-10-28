

import logging
import os
from functools import partial
import random
from pprint import pprint

import redis
from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_units_dict():
   with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
       file_contents = my_file.read()
       file_contents_split = file_contents.split('\n\n\n')

       units_dict = []

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


           units_dict.append(unit_dict)

       return units_dict



def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
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



# def echo_tg(units_dict , update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     keyboard_from_user = update.message.text
#
#     if keyboard_from_user == 'Новый вопрос':
#         unit_from_bot = random.choice(units_dict)
#         question_from_bot = unit_from_bot['Вопрос']
#         update.message.reply_text(question_from_bot)
#         host = "redis-19445.c52.us-east-1-4.ec2.redns.redis-cloud.com"
#         port = 19445
#         password = 'kx7oAwxlp7JMLjhpzzUyOEz1hFuqUQKe'
#         r = redis.Redis(host=host, port=port, password=password, decode_responses=True)
#         r.set(chat_id, question_from_bot)
#
#     elif keyboard_from_user == 'Сдаться':
#         answer = 'Точно сдаться?'
#         update.message.reply_text(answer)
#     elif keyboard_from_user == 'Мой счёт':
#         answer = 'Сделал запрос на Мой счёт'
#         update.message.reply_text(answer)


def get_new_q(units_dict, redis_object,  update: Update, context: CallbackContext):
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




def get_sdatsa(update: Update, context: CallbackContext):
    update.message.reply_text('Точно сдаться?__')

def get_my(update: Update, context: CallbackContext):
    update.message.reply_text('Сделал запрос на Мой счёт__')



def get_redis_start():
    host = "redis-19445.c52.us-east-1-4.ec2.redns.redis-cloud.com"
    port = 19445
    password = 'kx7oAwxlp7JMLjhpzzUyOEz1hFuqUQKe'
    redis_object = redis.Redis(host=host, port=port, password=password, decode_responses=True)
    return redis_object

def get_otvet(redis_object, update: Update, context: CallbackContext):

    otvet = redis_object.get('Ответ')
    word_from_user = update.message.text
    if word_from_user == otvet:
        update.message.reply_text('Это правльный ответ')

    else:
        update.message.reply_text(f'Это Не правльный ответ, верный ответ {otvet}')


def main():
    units_dict = get_units_dict()
    # pprint( questions_dict)
    # dict_up = questions_dict
    # print()
    # pprint(dict_up)
    #
    # random_index = random.randint(0, len(units_dict) - 1)
    # print('индекс', random_index)
    # unit = units_dict[random_index]
    # print('юнит',unit)
    # #
    # # dict_up.pop(random_index)
    # # pprint(dict_up)

    # print(redis_object.ping())
    #
    # print()
    # redis_object.mset(unit)
    # print('первый шаг', redis_object.keys())
    # print('первый шаг', redis_object.get('Вопрос'))
    # print('первый шаг', redis_object.get('Ответ'))

    # unit = random.choice(units_dict)
    # print(unit)
    # chat_id = 1
    #
    # unit = {'chat_id': chat_id}
    # redis_object.mset(unit)

    redis_object = get_redis_start()

    get_new_question = partial(get_new_q,  units_dict, redis_object)
    get_new_otvet = partial(get_otvet,   redis_object)

    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text('Новый вопрос'), get_new_question))
    dispatcher.add_handler(MessageHandler(Filters.text('Сдаться'), get_sdatsa))
    dispatcher.add_handler(MessageHandler(Filters.text('Мой счёт'), get_my))
    dispatcher.add_handler(MessageHandler(Filters.text, get_new_otvet))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()