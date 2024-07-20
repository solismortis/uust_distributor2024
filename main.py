me = '151-464-963 67'  # Необходимо выключать для Colab

# TODO: Добавить пустые приоритетные места к общему конкурсу
# TODO: Распределить приоритетный поток первым, не по приоритетам абитов
# TODO: Кнопка для тех, кто еще не подал доки
# TODO: Более правильное определение места по баллам
# TODO: Запилить вероятность поступления с учетом сдающих вступительные
# TODO: Сохранение в файл
# TODO: Коммерческий поток


import codecs
from pprint import pprint
import os
import re

import pandas as pd


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', None)


comp_groups = {}
def add_2_comp_groops(html):
    global comp_groups
    local_comp_groups = []
    fileObj = codecs.open(html, "r", "utf_8_sig")
    text = fileObj.read()
    text = text[re.search(r'<div class="list-specialty">.*</div>', text).end():]  # 1-й результат не наш

    for el in re.findall(r'<div class="list-specialty">.*</ul>', text):
        s = re.search(r'<li>Конкурсная группа: <span>.*</span></li>', el).group()
        start = re.search(r'<li>Конкурсная группа: <span>', s).end()
        end = re.search(r'</span>', s).start()
        comp_group = s[start:end]

        s = re.search(r'<li>Свободно мест: <span>\d+</span></li>', el).group()
        start = re.search(r'<li>Свободно мест: <span>', s).end()
        end = re.search(r'</span>', s).start()
        places = int(s[start:end])
        # print(places)

        # Всего есть 'Целевой прием', 'Полное возмещение затрат', 'Бюджетная основа'
        s = re.search(r'<li>Основание поступления: <span>.*</span></li>', el).group()
        start = re.search(r'<li>Основание поступления: <span>', s).end()
        end = re.search(r'</span>', s).start()
        basis = s[start:end]

        local_comp_groups.append({'comp_group': comp_group,
                                  'places': places,
                                  'basis': basis})

    def convert:


    tables_all = pd.read_html(html, converters={'Уникальный код': str})
    for i, df in enumerate(tables_all):
        local_comp_groups[i]['df'] = df[['Уникальный код',
                                         'Сумма балов',
                                         'Приоритет']].rename(columns={'Уникальный код': 'id',
                                                                       'Сумма балов': 'score',
                                                                       'Приоритет': 'prio'})

    # Удаляем коммерцию
    local_comp_groups1 = []
    for el in local_comp_groups:
        if el['basis'] != 'Полное возмещение затрат':
            local_comp_groups1.append(el)
    local_comp_groups = local_comp_groups1

    # Пихаем все в global comp_groups
    for el in local_comp_groups:
        comp_groups[el['comp_group']] = {'places': el['places'],
                                         'basis': el['basis'],
                                         'df': el['df']}


abits = {}
def create_abits():
    """ Создаем dict для приоритетов абитуриентов """
    for el_key, el_val in comp_groups.items():
        df = el_val['df']
        to_drop = []
        for index, row in df.iterrows():
            abit = row['id']
            if abit not in abits:
                abits[abit] = {}
                abits[abit][row['prio']] = {'comp_group': el_key, 'burnt': False}
            else:
                if row['prio'] in abits[abit]:  # Фикс бага с дубликатами прио
                    to_drop.append(index)
                else:
                    abits[abit][row['prio']] = {'comp_group': el_key, 'burnt': False}
        if to_drop:
            df.drop(to_drop)


my_comp_groups = []
my_score = None
def create_my_comp_groups():
    global my_comp_groups, my_score
    for el_key, el_val in comp_groups.items():
        df = el_val['df']
        df1 = df[df['id'] == me].dropna()
        if not df1.empty:
            my_comp_groups.append(el_key)
            my_score = int(df1['score'].iloc[0])
    # pprint(my_comp_groups)
    # print(f'Мои баллы: {my_score}')


def printmypos(distributed):
    """ Принт моих позиций. Ввиду того, как работает сортировка, на принт уйдет только позиция с зачислением,
    поэтому здесь также происходит поиск позиций по баллам в остальных группах. """
    groups = comp_groups if not distributed else sorted_groups
    print()
    if not distributed:
        print('Мои позиции до распределения')
    else:
        print('Мои позиции после распределения')
    for my_comp_group in my_comp_groups:
        df = groups[my_comp_group]['df']
        df1 = df[df['id'] == me].dropna()
        if not df1.empty:
            print(f'{my_comp_group}: {df1.index.tolist()[0] + 1}')
        else:
            for index, row in df[::-1].iterrows():  # Пихаем нас ниже того, у кого столько же или больше баллов
                if row.loc['score'] >= my_score:
                    print(f'{my_comp_group}: {index + 2}')
                    break
    print()


def sorting_algo(comp_groups, abits):
    """ Сортировка. Суть: псевдобесконечный луп по всем таблицам; в каждой выбираем всех вмещающихся абитов,
    смотрим их прио, если все прио перед ним сгорели (здесь под "сгорел" понимается вылет из конкурсной группы ввиду
    отсутствия мест), то зачисляем; убераем абита из остальных таблиц; если таблица обработана, выкидываем ее в
    sorted_groups. """
    sorted_groups = {}
    c = 0
    while comp_groups:
        to_pop = []
        for el_key, el_val in comp_groups.items():
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
                            if prio_val['comp_group'] != el_key:  # Только другие таблицы
                                try:
                                    df1 = comp_groups[prio_val['comp_group']]['df']
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
                #         for el2 in comp_groups:
                #             s = el2['Конкурсная группа'][:-len(x)-2]
                #             if s == s + ', Общая':
                #                 el2['Свободно мест'] += el['Свободно мест']
        c += 1
        for pop_el in to_pop:
            sorted_groups[pop_el] = comp_groups.pop(pop_el, None)
        print(f'Пробег №: {c}')
    return sorted_groups

# Пробегаемся по всем сохраненным html
files = os.listdir('./html files')
for filename in files:
    find = re.search(r'\.html', filename)
    if find:
        add_2_comp_groops('./html files/' + filename)

create_abits()
create_my_comp_groups()
printmypos(distributed=False)
sorted_groups = sorting_algo(comp_groups, abits)
printmypos(distributed=True)
# for my_comp_group in my_comp_groups:
#     print(my_comp_group)
#     print(sorted_groups[my_comp_group])
pass