# TODO: Функция для повторной обработки html
# TODO: Давать фронту список всех конкурсных групп для ввода для аналитики


import codecs  # Для HTML
import copy
import json
from pprint import pprint
import os
import re

import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)


def add_to_groups(html):
    """ Добавление групп из html в groups"""
    global groups
    local_groups = []
    fileObj = codecs.open(html, "r", "utf_8_sig")
    text = fileObj.read()
    text = text[re.search(r'<div class="list-specialty">.*</div>', text).end():]  # 1-й результат не наш

    for el in re.findall(r'<div class="list-specialty">.*</ul>', text):
        s = re.search(r'<li>Конкурсная группа: <span>.*</span></li>', el).group()
        start = re.search(r'<li>Конкурсная группа: <span>', s).end()
        end = re.search(r'</span>', s).start()
        group = s[start:end]

        s = re.search(r'<li>Свободно мест: <span>\d+</span></li>', el).group()
        start = re.search(r'<li>Свободно мест: <span>', s).end()
        end = re.search(r'</span>', s).start()
        places = int(s[start:end])

        # Всего есть 'Целевой прием', 'Полное возмещение затрат', 'Бюджетная основа'
        s = re.search(r'<li>Основание поступления: <span>.*</span></li>', el).group()
        start = re.search(r'<li>Основание поступления: <span>', s).end()
        end = re.search(r'</span>', s).start()
        basis = s[start:end]

        local_groups.append({'group': group,
                                  'places': places,
                                  'basis': basis})

    tables_all = pd.read_html(html, converters={'Уникальный код': str,
                                                'Приоритет': lambda el: int(re.search(r'\d*', el).group())})
    for i, df in enumerate(tables_all):
        local_groups[i]['df'] = df[['Уникальный код',
                                         'Сумма баллов',
                                         'Приоритет']].rename(columns={'Уникальный код': 'id',
                                                                       'Сумма баллов': 'score',
                                                                       'Приоритет': 'prio'})

    # Удаляем коммерцию
    local_groups1 = []
    for el in local_groups:
        if el['basis'] != 'Полное возмещение затрат':
            local_groups1.append(el)
    local_groups = local_groups1

    # Пихаем все в global groups
    for el in local_groups:
        groups[el['group']] = {'places': el['places'],
                                         'basis': el['basis'],
                                         'df': el['df']}


def create_abits():
    """ Создаем dict для приоритетов абитуриентов """
    abits = {}
    for el_key, el_val in original_groups.items():
        df = el_val['df']
        to_drop = []
        for index, row in df.iterrows():
            abit = row['id']
            if abit not in abits:
                abits[abit] = {}
                abits[abit][row['prio']] = {'group': el_key, 'burnt': False}
            else:
                if row['prio'] in abits[abit]:  # Фикс бага с дубликатами прио
                    to_drop.append(index)
                else:
                    abits[abit][row['prio']] = {'group': el_key, 'burnt': False}
        if to_drop:
            df.drop(to_drop)
    return abits


def process_id(id):
    """Обработка ID. Возвращает json"""
    # Поиск конкурсных групп и баллов выбранного абита
    id_groups = []
    id_score = None
    for el_key, el_val in original_groups.items():
        df = el_val['df']
        df1 = df[df['id'] == id].dropna()
        if not df1.empty:
            id_groups.append(el_key)
            id_score = int(df1['score'].iloc[0])

    # Обработка позиций id. Ввиду того, как работает сортировка, на принт уйдет только позиция с зачислением,
    # поэтому здесь также происходит поиск позиций по баллам в остальных группах
    arr = []
    for distributed in (False, True):
        dict0 = {}
        groups = original_groups if not distributed else sorted_groups
        if not distributed:
            dict0['text'] = f'Позиции id {id} до распределения:'
        else:
            dict0['text'] = f'Позиции id {id} после распределения:'
        dict0['groups'] = []
        for group in id_groups:
            df = groups[group]['df']
            df1 = df[df['id'] == id].dropna()  # Удаляет пустые строки?
            if not df1.empty:  # Срабатывает до распределения
                dict1 = {'group': group, 'pos': df1.index.tolist()[0] + 1}
                dict0['groups'].append(dict1)
            else:  # Срабатывает после распределения
                for index, row in df[::-1].iterrows():  # Пихаем нас ниже того, у кого столько же или больше баллов
                    if row.loc['score'] >= id_score:
                        dict1 = {'group': group, 'pos': index + 2}
                        dict0['groups'].append(dict1)
                        break
        arr.append(dict0)
    return json.dumps(arr, indent=4, ensure_ascii=False)


def sorting_algo(groups, abits):
    """ Сортировка. Делаем while loop по всем таблицам; в каждой выбираем всех вмещающихся абитов,
    смотрим их прио, если все прио перед этим прио сгорели (здесь под "сгорел" понимается вылет из конкурсной группы ввиду
    отсутствия мест), то зачисляем; убираем абита из остальных таблиц; если таблица обработана, выкидываем ее в
    sorted_groups """
    print('Сортировка\n')
    sorted_groups = {}
    c = 0
    while groups:
        to_pop = []
        for el_key, el_val in groups.items():
            places = el_val['places']
            df = el_val['df']
            sliced_df = df.iloc[:places]  # Выбираем только вмещающихся
            occupied = 0
            for index, row in sliced_df.iterrows():
                prio = row.loc['prio']
                if prio > 0:  # 0 = поступил, -1 = вылетел
                    abit = row.loc['id']
                    can_use_prio = True
                    for p in range(1, prio):
                        try:
                            if not abits[abit][p]['burnt']:  # Если предыдущие прио не сгорели
                                can_use_prio = False
                                break
                        except KeyError:  # Для поломанных прио, как то [1, 4, 5] вместо [1, 2, 3]
                            pass
                    if can_use_prio:
                        df.loc[index, 'prio'] = 0  # Поступил
                        occupied += 1
                        # Убираем этого абитуриента из остальных таблиц
                        for prio_key, prio_val in abits[abit].items():
                            prio_val['burnt'] = True  # Сжечь все
                            if prio_val['group'] != el_key:  # Только другие таблицы
                                try:
                                    df1 = groups[prio_val['group']]['df']
                                    df2 = df1[df1['id'] == abit].dropna()
                                    if not df2.empty:
                                        i = df2.index
                                        df1.drop(i, inplace=True)
                                        df1.reset_index(drop=True, inplace=True)
                                except KeyError:  # Уже в sorted_groups:
                                    pass
                else:
                    occupied += 1
            # Мест больше нет, либо больше нет абитов
            try:
                zeros_c = df['prio'].value_counts().iloc[0]
            except (KeyError, IndexError) as e:
                zeros_c = 0
            if occupied == places or df.empty or zeros_c == df.shape[0]:
                df3 = df.iloc[places:]
                for index, row in df3.iterrows():
                    abit = row['id']
                    df.loc[index, 'prio'] = -1  # Вылет
                    for prio_key, prio_val in abits[abit].items():  # Сжечь все
                        prio_val['burnt'] = True
                # Выкинуть таблицу в sorted_group
                to_pop.append(el_key)
                # Освободить место:
                # Может быть такое: 09.03.04 Программная инженерия, Очная, Бюджет, Целевая, СЭГЗ АО
                # for x in ['особая', 'отдельная', 'целевая']:
                #     if x in el['Конкурсная группа']:
                #         for el2 in groups:
                #             s = el2['Конкурсная группа'][:-len(x)-2]
                #             if s == s + ', Общая':
                #                 el2['Свободно мест'] += el['Свободно мест']
        c += 1
        for pop_el in to_pop:
            sorted_groups[pop_el] = groups.pop(pop_el, None)
        print(f'Пробег №: {c}')
    print()
    return sorted_groups


groups = {}  # Основной dict для конкурсных групп. Очищается по мере сортировки
original_groups = {}

def process_html():
    """ Парсинг html """
    global groups
    global original_groups
    # Пробегаемся по всем сохраненным html
    files = os.listdir('./html files')
    for filename in files:
        find = re.search(r'\.html', filename)
        if find:
            add_to_groups('./html files/' + filename)
    original_groups = copy.deepcopy(groups)

process_html()

abits = create_abits()
sorted_groups = sorting_algo(groups, abits)

json_object = process_id(id='151-464-963 67')
print(json_object)

json_object = process_id(id='139-925-279 07')
print(json_object)

# Аналитика
# def return_processed_groups(groups_of_interest):
#     arr = []
#     for group in groups_of_interest:
#         group1 = copy.deepcopy(sorted_groups[group])
#         group1['df'] = group1['df'].values.tolist()
#         arr.append(group1)
#     return json.dumps(arr, indent=4, ensure_ascii=False)
#
# groups_of_interest = ['02.03.03 Технологиии искусственного интеллекта, Очная, Бюджет, Общая',
#                       '03.03.01 Моделирование физических процессов и технологий, Очная, Бюджет, Отдельная',
#                       '06.03.01 Общая биология (Сибайский институт), Очная, Бюджет, Общая']
# print(return_processed_groups(groups_of_interest))
pass
