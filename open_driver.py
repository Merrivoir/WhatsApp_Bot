# импорт системных модулей
import random
import urllib
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

#импорт собственных модулей
from CFMessages import ColdBaseMsg
from CFNumbers import coldbase

# XPath для модального окна и текста сообщения
modal_xpath = '//*[@data-animate-modal-popup="true"]'
message_xpath = '//*[@data-animate-modal-body="true"]//div[@class="x12lqup9 x1o1kx08"]'

print(f"----------------------------------------------------------------------------")
print(f"Скрипт open_driver начал работу")

options = webdriver.FirefoxOptions()

options.add_argument('-profile')
options.add_argument('C:\\Msync\\profiles\\firefox\\77757468937')

print(f"Браузер запускается")
driver = webdriver.Firefox(options=options)

def Logger(text):
    with open("Log/CFCB.txt", "a", encoding='utf-8') as file:
        file.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {text}\n\n")

def sendMessage():
    driver.find_element(By.XPATH, '//button[@data-tab="11"]').click()
    sleep(5)

testNumbers = ["77474728450","77777777777","77757468937","77089287735"]
unregistered = []

for number in testNumbers:
    print(f"Обработка номера: {number}")
    msg = random.choice(ColdBaseMsg)
    encodedString = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={number}&text={encodedString}"
    driver.get(url)
    #sleep(3000)
    sleep(3)

    try:
        # Ожидаем появления модального окна
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))
        print("Загрузка чата")

        # Ожидание исчезновения модального окна
        try:
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.XPATH, modal_xpath)))
            print("Модальное окно исчезло. Выполняем действия на странице.")
            Logger(f"Сообщение для номера {number}\n{msg}")
            sleep(3)
            # Ваши действия здесь
            sendMessage()
            next  # Успешно выполнили действия, переходим к следующему номеру

        except TimeoutException:
            # Модальное окно не исчезло в течение 30 секунд, читаем текст
            print("Модальное окно не исчезло, проверяем текст...")
            modal_text = None
            try:
                message_elem = driver.find_element(By.XPATH, message_xpath)
                modal_text = message_elem.get_attribute("innerText") or message_elem.text
                print("Текст модального окна:", modal_text)

                # Обработка текста модального окна
                if "недействительный" in modal_text.lower():
                    print(f"Номер {number} не зарегистрирован")
                    Logger(f"Номер {number} не зарегистрирован")
                    unregistered.append(number)
                    next  # Выходим, чтобы перейти к следующему `number` в `coldbase`

                elif "что ваш компьютер подключен" in modal_text.lower():
                    print("Проблемы с соединением. Повторная попытка через 10 минут.")
                    Logger(f"Проблемы с загрузкой чата, пауза...")
                    sleep(600)  # Пауза на 600 секунд (10 минут)
                    continue  # Повторяем попытку для этого же номера после паузы

            except (StaleElementReferenceException, NoSuchElementException):
                print("Не удалось получить текст модального окна.")
                next  # При ошибке завершаем обработку текущего номера

    except Exception as e:
        print("Ошибка:", e)
        Logger(f"{number}\n{e}")
        next  # Завершаем внутренний цикл при других ошибках и переходим к следующему `number`

