import os
import random

def get_quiz():
    folder_for_quiz_questions = 'quiz-questions'
    files_with_quiz_questions = os.listdir(folder_for_quiz_questions)
    file_with_quiz_questions = random.choice(files_with_quiz_questions)
    with open(f'{folder_for_quiz_questions}/{file_with_quiz_questions}', "r", encoding="KOI8-R") as my_file:
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
