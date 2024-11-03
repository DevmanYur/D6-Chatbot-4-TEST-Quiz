import re
import string


def get_questions_dict():
   with open('1vs1299.txt', "r", encoding="KOI8-R") as my_file:
       file_contents = my_file.read()
       file_contents_split = file_contents.split('\n\n\n')

       questions_dict = []

       for questions_and_answers in  file_contents_split:
           question_and_answer = questions_and_answers.split('\n\n')
           print(question_and_answer)
           for x in question_and_answer:

               if "Вопрос " in x:
                   print('Это вопрос')
                   ind_ = x.find(':')+1
                   line = x[:ind_]
                   numbers = re.findall(r'\b\d+\b', line)
                   print(numbers)
                   print(x[ind_:])
                   print()






                   print()
               # if "Ответ:" in x:
               #     print('Это ответ')
               #     print(x)
               #     print()

           print()
           print()

           # question_fields, answer_fields, source_fields, author_fields = question_and_answer
           #
           # question_field, question =  question_fields.split('\n')
           # answer_field, answer = answer_fields.split('\n')
           # source_field, source = source_fields.split('\n')
           # author_field, author = author_fields.split('\n')
           #
           # question_dict = {'Вопрос': question,
           #                  'Ответ': answer,
           #                  'Источник': source,
           #                  'Автор': author}
           #
           #
           # questions_dict.append(question_dict)

       return questions_dict




get_questions_dict()