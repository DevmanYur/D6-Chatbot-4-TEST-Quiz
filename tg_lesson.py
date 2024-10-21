
# импортируем обработчик CommandHandler,
# который фильтрует сообщения с командами
from telegram.ext import CommandHandler, CallbackQueryHandler

# импортируем обработчик `MessageHandler` и класс с фильтрами
from telegram.ext import MessageHandler, Filters


from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import InlineQueryHandler
import logging
import os
from functools import partial
import random
from pprint import pprint

import redis
from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CallbackContext

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


#
# # Обратите внимание, что из обработчика в функцию
# # передаются экземпляры `update` и `context`
# def start(update, context):
#     # `bot.send_message` это метод Telegram API
#     # `update.effective_chat.id` - определяем `id` чата,
#     # откуда прилетело сообщение
#     context.bot.send_message(chat_id=update.effective_chat.id,
#                              text="I'm a bot, please talk to me!")


# https://docs-python.ru/packages/biblioteka-python-telegram-bot-python/menju-klaviatury/
def start(update, _):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # для версии 13.x
    update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)
    # для версии 20.x необходимо использовать оператор await
    # await update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)

# функция обратного вызова
def echo(update, context):
    # добавим в начало полученного сообщения строку 'ECHO: '
    text = 'ECHO: ' + update.message.text
    # `update.effective_chat.id` - определяем `id` чата,
    # откуда прилетело сообщение
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)

'''
Добавим боту другую функциональность и реализуем команду /caps, 
которая будет принимать какой-то текст в качестве аргумента 
и отвечать на него тем же текстом, 
только в верхнем регистре. 
Аргументы команды (например /caps any args) 
будут поступать в функцию обратного вызова в виде списка ['any', 'args'],
разделенного по пробелам:
'''
def caps(update, context):
    # если аргументы присутствуют
    if context.args:
        # объединяем список в строку и
        # переводим ее в верхний регистр
        text_caps = ' '.join(context.args).upper()
        # `update.effective_chat.id` - определяем `id` чата,
        # откуда прилетело сообщение
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text_caps)
    else:
        # если в команде не указан аргумент
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='send: /caps argument')


'''
Режим встроенных запросов.
Если встроенные запросы включены, 
то пользователи могут вызвать бота, 
введя его имя @bot_username и запрос в поле ввода текста в любом чате. 
Запрос отправляется боту в обновлении. 
Таким образом, люди могут запрашивать контент у ботов в любом из своих чатов, 
групп или каналов, вообще не отправляя 
им никаких отдельных сообщений.
'''

def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Convert to UPPER TEXT',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

'''
Пользователи могут попытаться отправить боту команды,
 которые он не понимает, поэтому можно использовать 
 обработчик MessageHandler с фильтром Filters.command, 
 чтобы отвечать на все команды, которые не были распознаны предыдущими обработчиками.
 
 Примечание. Этот обработчик должен быть добавлен последним. 
 Если его поставить первым, то он будет срабатывать до того, 
 как обработчик CommandHandlers для команды /start увидит обновление. 
 После обработки обновления функцией unknown() 
 все дальнейшие обработчики будут игнорироваться.
 Остановить бота можно командой updater.stop().
'''
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def button(update, _):
    query = update.callback_query
    variant = query.data

    # `CallbackQueries` требует ответа, даже если
    # уведомление для пользователя не требуется, в противном
    #  случае у некоторых клиентов могут возникнуть проблемы.
    # смотри https://core.telegram.org/bots/api#callbackquery.
    query.answer()
    # для версии 20.x необходимо использовать оператор await
    # await query.answer()

    # редактируем сообщение, тем самым кнопки
    # в чате заменятся на этот ответ.
    query.edit_message_text(text=f"Выбранный вариант: {variant}")
    # для версии 20.x необходимо использовать оператор await
    # await query.edit_message_text(text=f"Выбранный вариант: {variant}")

def help_command(update, _):
    update.message.reply_text("Используйте `/start` для тестирования.")
    # для версии 20.x необходимо использовать оператор await
    # await update.message.reply_text("Используйте `/start` для тестирования.")


if __name__ == '__main__':
    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']

        # получаем экземпляр `Updater`
    updater = Updater(token=telegram_token, use_context=True)

        # получаем экземпляр `Dispatcher`
    dispatcher = updater.dispatcher

        # говорим обработчику, если увидишь команду `/start`,
        # то вызови функцию `start()`
    start_handler = CommandHandler('start', start)

        # добавляем этот обработчик в `dispatcher`
    dispatcher.add_handler(start_handler)

        # обработчик текстовых сообщений
        # говорим обработчику `MessageHandler`, если увидишь текстовое
        # сообщение (фильтр `Filters.text`)  и это будет не команда
        # (фильтр ~Filters.command), то вызови функцию `echo()`
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
        # регистрируем обработчик `echo_handler` в экземпляре `dispatcher`
    dispatcher.add_handler(echo_handler)

        # обработчик команды '/caps'
    caps_handler = CommandHandler('caps', caps)
        # регистрируем обработчик в диспетчере
    dispatcher.add_handler(caps_handler)

    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler('help', help_command))

        # обработчик встроенных запросов
    inline_caps_handler = InlineQueryHandler(inline_caps)
    dispatcher.add_handler(inline_caps_handler)

        # обработчик не распознанных команд
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)


        # говорим экземпляру `Updater`,
        # слушай сервера Telegram.
    updater.start_polling()

        # обработчик нажатия Ctrl+C
    updater.idle()