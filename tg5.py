

import logging
import os
from functools import partial
import random
from pprint import pprint

from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_questions_dict():
   with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
       file_contents = my_file.read()
       file_contents_split = file_contents.split('\n\n\n')

       questions_dict = []

       for questions_and_answers in  file_contents_split:
           question_and_answer = questions_and_answers.split('\n\n')
           question_fields, answer_fields, source_fields, author_fields = question_and_answer

           question_field, question =  question_fields.split('\n')
           answer_field, answer = answer_fields.split('\n')
           source_field, source = source_fields.split('\n')
           author_field, author = author_fields.split('\n')

           question_dict = {'Вопрос': question,
                            'Ответ': answer,
                            'Источник': source,
                            'Автор': author}


           questions_dict.append(question_dict)

       return questions_dict



def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

    #########################

    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        text="Custom Keyboard Test",
        reply_markup=reply_markup)


##########################3


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

#########################

    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
                     text="Custom Keyboard Test",
                     reply_markup=reply_markup)

##########################3


def echo_tg(questions_dict , update: Update, context: CallbackContext):
    q = update.message.text
    dict_up = questions_dict
    if q == 'Новый вопрос':


        answer = random.choice(questions_dict['Вопрос'])
        update.message.reply_text(answer)
    elif q == 'Сдаться':
        answer = 'Точно сдаться?'
        update.message.reply_text(answer)
    elif q == 'Мой счёт':
        answer = 'Сделал запрос на Мой счёт'
        update.message.reply_text(answer)


def main():
    questions_dict = get_questions_dict()
    pprint( questions_dict)
    dict_up = questions_dict
    print()
    pprint(dict_up)

    random_index = random.randint(0, len(questions_dict) - 1)
    pprint(random_index)
    answer = questions_dict[random_index]
    print(answer)

    dict_up.pop(random_index)
    pprint(dict_up)
    # echo = partial( echo_tg, questions_dict)
    #
    # load_dotenv()
    # telegram_token = os.environ['TG_TOKEN']
    #
    # updater = Updater(telegram_token)
    #
    # # Get the dispatcher to register handlers
    # dispatcher = updater.dispatcher
    #
    # # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    #
    # # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    #
    # # Start the Bot
    # updater.start_polling()
    #
    # # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # # SIGTERM or SIGABRT. This should be used most of the time, since
    # # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()
    #

if __name__ == '__main__':
    main()