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
import threading
import time

def update_html():
    while True:
        print("Ожидание...")
        now = datetime.now()
        if now.strftime("%H:%M") == "02:00":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            driver = webdriver.Firefox(options = options)

            url = "https://list.uust.ru/spisok.php?levelTarget=vo_rang&specialty=&original=originalAll&search_type=snils&snls="
            driver.get(url)
            print("Началось обновление html")
            for i in range(3,111): #здесь нужно указать от трех до числа специальностей (Ввести: 111)
                search_box = driver.find_element(By.NAME, "specialty")
                search_box.click()

                search_box = driver.find_element(By.CSS_SELECTOR, f"div.list-filter-element4:nth-child(3) > select:nth-child(1) > option:nth-child({i})")
                spec_name = search_box.get_attribute("value")
                search_box.click()
                html_update = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")

                html_old = open(f"selenium html files/{spec_name}.html", "w+", encoding="utf-8") #сохраняет html в другую папку
                html_old.write(html_update)
                html_old.close()

                search_box = driver.find_element(By.NAME, "specialty")
                search_box.click()

                search_box = driver.find_element(By.CSS_SELECTOR, "div.list-filter-element4:nth-child(3) > select:nth-child(1) > option:nth-child(2)")
                search_box.click()
            driver.quit()
            print("Обновление завершилось")
        time.sleep(60)

serv=Flask(__name__)
CORS(serv)
@serv.route('/')
def home():
    return "Server is online now"

@serv.route('/search')
def serc():
    user = request.args.get('id')
    return main.process_id(user)

def start_background_task():
    thread = threading.Thread(target=update_html, daemon=True)
    thread.start()

if __name__ == "__main__":
    start_background_task()
    serv.run(debug=True, use_reloader=False)
