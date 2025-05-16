""" Файл для тестирования работы original.py.
Чтобы не засорять консоль сервера при запуске. Для Марселя. """

import original


original.process_html_and_sort()

# Проверка обработки ID
json_object = original.process_id(id='151-464-963 67')
print(json_object)

json_object = original.process_id(id='139-925-279 07')
print(json_object)


# Проверка аналитики
# print(original.list_of_all_groups)

groups_of_interest = ['02.03.03 Технологиии искусственного интеллекта, Очная, Бюджет, Общая',
                      '03.03.01 Моделирование физических процессов и технологий, Очная, Бюджет, Отдельная',
                      '06.03.01 Общая биология (Сибайский институт), Очная, Бюджет, Общая']
print(original.return_processed_groups(groups_of_interest))