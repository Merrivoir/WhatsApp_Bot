from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException
from time import sleep
from datetime import datetime
import urllib.parse
import random

waXPInputArea = "//div[@data-testid='conversation-compose-box-input']"

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

element = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="+7 700 299 0331"]'))
)
element.click()

elements_akbu = driver.find_elements(By.CLASS_NAME, "_akbu")                        # Находим все элементы <div class="_akbu">

if elements_akbu:                                                                   # Проверяем, что есть элементы
    
    last_akbu = elements_akbu[-1]                                                   # Получаем последний элемент <div class="_akbu">
    
    links = last_akbu.find_elements(By.CLASS_NAME, "_ao3e")                         # Находим все ссылки <a class="_ao3e selectable-text copyable-text"> внутри последнего элемента
    
    for link in links:                                                              # Проходим по всем ссылкам
        try:
            link.click()
            sleep(1)
            try:
                phone_popup = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "_ak4w"))
                )
                phone_text = phone_popup.text           
                if "+7" in phone_text:                                              # Проверяем, содержится ли номер телефона внутри элемента
                    print("Телефон зарегистрирован")
                else:
                    print("Данный номер не зарегистрирован")
            except:
                print("Всплывающее окно с телефоном не найдено.")
        except Exception as e:
            print(f"Ошибка при переходе по ссылке: {e}")
else:
    print("Элементы <div class='_akbu'> не найдены.")