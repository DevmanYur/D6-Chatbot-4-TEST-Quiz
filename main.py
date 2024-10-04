
with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
  file_contents = my_file.read()
# print(file_contents)

letters = "⌡"
rawdata = letters.encode("KOI8-R")
# print(rawdata)


def f1():
   with open('1vs1201_.txt', "r", encoding="KOI8-R") as my_file:
     for line in my_file:
         if line == '\n':
             print("перенос2")
         print(line)

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