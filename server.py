from calendar import day_name
from datetime import datetime

from flask_cors.core import serialize_option
from numpy.f2py.rules import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import *
from flask_cors import CORS
import json
import main
import original
import threading
import time

main.process_html_and_sort()
original.process_html_and_sort()

def update():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    names_old = open(f"selenium group names.txt", "w+", encoding="utf-8")
    names = []

    url = "https://list.uust.ru/spisok.php?levelTarget=vo_rang&specialty=&original=originalAll&search_type=snils&snls="
    driver.get(url)
    print("Началось обновление html")

    spec_list = driver.find_elements(By.CSS_SELECTOR,
                                     "div.list-filter-element4:nth-child(3) > select:nth-child(1) > option")
    for i in range(3, len(spec_list) + 1):
        search_box = driver.find_element(By.NAME, "specialty")
        search_box.click()
        #   <<< Поиск названия специальности для создания соответствующего файла >>>
        search_box = driver.find_element(By.CSS_SELECTOR,
                                         f"div.list-filter-element4:nth-child(3) > select:nth-child(1) > option:nth-child({i})")
        spec_name = search_box.get_attribute("value")
        search_box.click()
        html_update = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")  # Парсинг HTML

        #   << дополнительно парсинг названий конкурсных групп >>
        spans = driver.find_elements(By.CSS_SELECTOR, "ul.list-head > li:nth-child(3) > span:nth-child(1)")
        for span in spans:
            names.append(span.text)

        for name in names:
            if "Контракт" in name:
                continue
            names_old.write(name + '\n')
        names.clear()

        #   <<< создание(или перезапись если такой файл есть) файла с соответствующим названием >>>
        html_old = open(f"selenium html files/{spec_name}.html", "w+",
                        encoding="utf-8")  # сохраняет html в другую папку
        html_old.write(html_update)
        html_old.close()
        #   <<< Возвращение на страницу со всеми специальностями >>>
        search_box = driver.find_element(By.NAME, "specialty")
        search_box.click()
        search_box = driver.find_element(By.CSS_SELECTOR,
                                         "div.list-filter-element4:nth-child(3) > select:nth-child(1) > option:nth-child(2)")
        search_box.click()
    names_old.close()
    driver.quit()
    print("Началось обновление списков")
    main.process_html_and_sort()
    original.process_html_and_sort()
    print("Обновления завершились")

def update_html():
    while True:
        print("Ожидание...")
        now = datetime.now()
        if now.strftime("%H") == "02":
            update()
        time.sleep(3600)

serv=Flask(__name__)
CORS(serv)
@serv.route('/')
def home():
    return "Server is online now"

@serv.route('/search')
def serc():
    user = request.args.get('id')
    return main.process_id(user)

# Все группы
all_groups = []
f = open("selenium group names.txt", "r", encoding="utf-8")
groups = f.readlines()
for group in groups:
    all_groups.append(group.strip())

# Построим map: направление -> группы
direction_map = {}
for group in all_groups:
    code = group.split()[0]
    direction_map.setdefault(code, []).append(group)

@serv.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        selected_groups = request.form.getlist('group')
        expanded_dirs = request.form.get('expanded_dirs', '').split(',')
    else:
        selected_groups = []
        expanded_dirs = []

    return render_template(
        'menu.html',
        direction_map=direction_map,
        selected_groups=selected_groups,
        expanded_dirs=expanded_dirs
    )

@serv.route('/analytAll', methods=['POST'])
def analyt_all():
    selected_groups = request.form.getlist('group')  # выбранные конкурсные группы
    selected_dirs = request.form.getlist('dir')      # направления (флажки на кодах)

    # Автоматически добавляем все конкурсные группы, если флажок на направлении, но группы не выбраны
    for code in selected_dirs:
        if not any(group.startswith(code) for group in selected_groups):
            selected_groups.extend(direction_map.get(code, []))

    json_str_all = main.return_processed_groups(selected_groups)
    data_all = json.loads(json_str_all)
    return render_template('Analyt_table.html', data=data_all, orig=False)

@serv.route('/analytOrig', methods=['POST'])
def analyt_orig():
    selected_groups = request.form.getlist('group')
    selected_dirs = request.form.getlist('dir')

    for code in selected_dirs:
        if not any(group.startswith(code) for group in selected_groups):
            selected_groups.extend(direction_map.get(code, []))

    json_str_orig = original.return_processed_groups(selected_groups)
    data_orig = json.loads(json_str_orig)
    return render_template('Analyt_table.html', data=data_orig, orig=True)

def start_background_task():
    thread = threading.Thread(target=update_html, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_background_task()
    serv.run(debug=True, use_reloader=False)
