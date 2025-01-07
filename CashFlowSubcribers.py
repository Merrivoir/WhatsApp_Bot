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
from CFMessages import msg_marathon
from CFNumbers import numbers_marathon

# XPath для модального окна и текста сообщения
modal_xpath = '//*[@data-animate-modal-popup="true"]'
message_xpath = '//*[@data-animate-modal-body="true"]//div[@class="x12lqup9 x1o1kx08"]'
dailyAtt = 10 #количество номеров для обработки за день

print(f"----------------------------------------------------------------------------")
print(f"Скрипт open_driver начал работу - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

options = webdriver.FirefoxOptions()

options.add_argument('-profile')
options.add_argument('C:\\Msync\\profiles\\firefox\\77058893755')

print(f"Браузер запускается")
driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/" #загрузка для синхронизации
driver.get(url)

def Logger(text):
    with open("Log/CFCB.txt", "a", encoding='utf-8') as file:
        file.write(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | {text}\n\n")

def sendMessage(status = False): #отправка сообщения
    try:
        # Находим кнопку отправки сообщения
        driver.find_element(By.XPATH, '//button[@data-tab="11"]').click()
        if status:
            sleep(10)
            # Находим последний элемент <div class="" role="row">
            rows = driver.find_elements(By.XPATH, '//div[@role="row"]')
            last_row = rows[-1]  # Получаем последний элемент

            # Ищем внутри него элемент <span> с указанным атрибутом
            span = last_row.find_element(By.XPATH, './/span[@aria-hidden="false"][@data-icon]')

            # Считываем значение атрибута aria-label
            aria_label = span.get_attribute("aria-label").strip()
            print("Статус сообщения:", aria_label)

            return aria_label
        else:
            sleep(3)
            return True

    except Exception as e:
        print("Ошибка при отправке сообщения:", e)
        return None

testNumbers = ["77474728450","77777777777","77757468937","77089287735"]
unregistered = []

for number in numbers_marathon:
    print(f"Обработка номера: {number}")
    #msg = random.choice(ColdBaseMsg)
    encodedString = urllib.parse.quote(msg_marathon)
    url = f"https://web.whatsapp.com/send?phone={number}" #&text={encodedString}"
    driver.get(url)
    #sleep(3000)
    sleep(10)

    try:
        # Ожидаем появления модального окна
        print("Загрузка чата")
        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))

        # Ожидание исчезновения модального окна
        try:
            WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.XPATH, modal_xpath)))
            print("Выполняем действия на странице.")
            sleep(10)
            # Ваши действия здесь
            #status = sendMessage(True)
            #Logger(f"Сообщение для номера {number}\n{msg}\nСтатус: {status}")
            #print("Готово. Следующее через 4 минуты")
            #sleep(245)
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
                    sleep(3)
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

print(f"Незарегистрированные номера:\n{unregistered}\n")
print(f"----------------------------------------------------------------------------")
print(f"Скрипт open_driver завершил работу - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

