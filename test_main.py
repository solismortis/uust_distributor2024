""" Файл для тестирования работы main.py.
Чтобы не засорять консоль сервера при запуске. Для Марселя. """

import main
import original


main.process_html_and_sort()

# Проверка обработки ID
json_object = main.process_id(id='151-464-963 67')
#print(json_object)

json_object = main.process_id(id='139-925-279 07')
#print(json_object)


# Проверка аналитики
#print(main.list_of_all_groups)

groups_of_interest = [
                        '01.03.02 Искусственный интеллект и анализ данных (Стерлитамакский филиал), Очная, Бюджет, Особая',
                        '02.03.03 Технологиии искусственного интеллекта, Очная, Бюджет, Отдельная',
                        '03.03.01 Моделирование физических процессов и технологий, Очная, Бюджет, Отдельная']
print(main.return_processed_groups(groups_of_interest))