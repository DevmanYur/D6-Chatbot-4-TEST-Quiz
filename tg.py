import logging
import os

import telegram
from dotenv import load_dotenv
from telegram import Update, ForceReply, InlineKeyboardMarkup, bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from typing import Union, List
from telegram import InlineKeyboardButton

logger = logging.getLogger(__name__)


def get_command_start_tg(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет {user.mention_markdown_v2()}',
        reply_markup=ForceReply(selective=True),
    )

def get_answer1(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu



def get_answer(update: Update, context: CallbackContext ) -> None:
    question = update.message.text
    chat_id = update.message.chat_id
    update.message.reply_text(text=question)


def get_answer2(update: Update, context: CallbackContext ) -> None::
    custom_keyboard = [['top-left', 'top-right'],
                       ['bottom-left', 'bottom-right']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Custom Keyboard Test",
                     reply_markup=reply_markup)



def start_tg_bot(telegram_token):
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", get_command_start_tg))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,get_answer))
    updater.start_polling()
    updater.idle()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    load_dotenv()
    telegram_token = os.environ['TG_TOKEN']
    start_tg_bot(telegram_token)

if __name__ == '__main__':
    main()
