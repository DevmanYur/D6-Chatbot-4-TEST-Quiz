import logging
import os

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import redis

from quiz import get_quiz

logger = logging.getLogger(__name__)



def get_units():
   with open('1vs1299.txt', "r", encoding="KOI8-R") as my_file:
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


def start_vk_bot(vk_community_token, redis_object, units):
    vk_session = vk.VkApi(token=vk_community_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счёт', color=VkKeyboardColor.PRIMARY)


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:

            if event.text == "Новый вопрос":
                unit = random.choice(units)
                redis_object.mset(unit)
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=f'{unit['Вопрос']}',
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000))

            if event.text == redis_object.get('Ответ'):
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=f'Супер - это правильный ответ',
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000))

            if event.text == "Сдаться":
                answer = redis_object.get('Ответ')
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=f'Окей, правильный ответ - {answer}',
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000)
                )
    VkLongPoll(vk_session)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()

    vk_community_token = os.environ['VK_TOKEN']
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    redis_object = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    units = get_quiz()

    start_vk_bot(vk_community_token, redis_object, units)


if __name__ == '__main__':
    main()