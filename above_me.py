""" Заброшенный файл.

Gives a very rough approximation of my chances by providing how many unique IDs are above me."""

import pandas as pd


me = '151-464-963 67'

tables_all = pd.read_html('ИИМРТ.html')

above_me = pd.DataFrame()
for df in tables_all:
    row = df.loc[df['Уникальный код'] == me]
    if not row.empty:
        i = row.index[0]
        above_me = pd.concat([above_me, df.iloc[:i]])
above_me = above_me['Уникальный код']
print(f'Unique above me: {len(above_me.unique())}')
print('Total min: 222')
print('Total max: 339')