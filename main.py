

with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
  file_contents = my_file.read()
# print(file_contents)

letters = "⌡"
rawdata = letters.encode("KOI8-R")
# print(rawdata)


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



       #     for yyy  in sp2:
       #         # sp3 = y.split('\n'),
       #         print(yyy)
       #         print()
       # #
       #         print()








           # for y in sp2:
           #     # dict1 = dict()
           #     # dict1['Вопрос'] = ['Name']
           #     sp3 = y.split('\n')
           #     print(sp3)
           #     print()
           #
           #     # print(sp3[0:1])
           #     # print(sp3[1:2])



     # for line in my_file:
     #     if line == '\n\n':
     #         print("перенос2")
     #     print(line)

         # for lett in line:
         #     if lett == '\n':
         #         print("перенос2")
         #
         #
         #
         #     rawdata = lett.encode("KOI8-R")
         #     print(rawdata)
         #     if rawdata == b'\n':
         #         print("перенос")
      # my_str = line
      # simvols = ['/', '-', '(', ')', 'х ф', '.', ',', '"', "'", '?', '!', 'х ф', 'м ф', 'д ф', 'к п', 'т п', 'т ф',
      #            'к ф', 'ф сп', 'науч поп ф', 'т спек', 'ф концерт', 'т с', 'ф к', 'к с им Горького', 'Культура ФГУП',
      #            '…', ' ПД', '_', 'Острова', '№', 'Т программа', 'Документальные фильмы', 'озвуч', 'вып', 'серия',
      #            'выпуск', 'Сезон',
      #            'сезон', 'часть', 'фильм', 'озв ', 'уск ']
      # for simvol in simvols:
      #   my_str = my_str.replace(simvol, ' ')
      #   if "  " in my_str:
      #     my_str = my_str.replace('  ', ' ')
      #   sanitize_my_str = sanitize_filename(my_str.strip())
      # sanitize.write(sanitize_my_str + '\n')

f1()