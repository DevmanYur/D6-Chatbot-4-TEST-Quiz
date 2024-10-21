# https://mastergroosha.github.io/telegram-tutorial/docs/lesson_01/

from telegram import bot


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.infinity_polling()