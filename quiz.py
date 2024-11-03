import re
import string
from pprint import pprint


def get_quiz():
    with open('1vs1299.txt', "r", encoding="KOI8-R") as my_file:
        file_contents = my_file.read()
        units = file_contents.split('\n\n\n')
        quiz = []
        for unit in units:
            parts = unit.split('\n\n')
            for part in parts:
                if "Вопрос " in part:
                    index_symbol = part.find(':')+2
                    question = part[index_symbol:]
                if "Ответ:" in part:
                    index_symbol = part.find(':')+2
                    answer = part[index_symbol:]
            part_of_quiz = {'Вопрос': question,
                            'Ответ': answer}
            quiz.append(part_of_quiz)

        return quiz




pprint(get_quiz())