from numpy.f2py.rules import options
from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import *
from flask_cors import CORS
import json
import main

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options = options)

url = "https://list.uust.ru/spisok.php?levelTarget=bak&specialty=01.03.02+%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0&footings=%D0%91%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%D0%BD%D0%B0%D1%8F+%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B0&search_type=snils&snls=17399553731&group=01.03.02+%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82+%D0%B8+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D0%B7+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85+%28%D0%A1%D1%82%D0%B5%D1%80%D0%BB%D0%B8%D1%82%D0%B0%D0%BC%D0%B0%D0%BA%D1%81%D0%BA%D0%B8%D0%B9+%D1%84%D0%B8%D0%BB%D0%B8%D0%B0%D0%BB%29%2C+%D0%9E%D1%87%D0%BD%D0%B0%D1%8F%2C+%D0%91%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%2C+%D0%9E%D0%B1%D1%89%D0%B0%D1%8F&profile="
driver.get(url)

html = driver.find_element(By.TAG_NAME, "html").get_attribute("outerHTML")
print(html)


serv=Flask(__name__)
CORS(serv)

@serv.route('/search')
def serc():
    user = request.args.get('id')
    return main.process_id(user)

if __name__ != "__main__":
    serv.run()