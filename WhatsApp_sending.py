from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as By
from selenium.webdriver.support.ui import WebDriverWait as WDWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from time import sleep
from datetime import datetime
import urllib.parse
import random

#блок импорта номеров и сообщений
from Aiqerim import nm_aq as numbers
from Aiqerim import message_aq1 as message
from CFMessages import msg_t1 as msg
from CFMessages import phoneNumbers1 as numbers

#Элементы на странице
modal_elem = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
modal_btn = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button'
#send_btn = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button'
send_btn = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button'

defaultDelay = 30
phonenumber = input("Введите номер от имени которого нужна рассылка: ")
delay = input(f"Введите значение задержки (по умолчанию {defaultDelay}): ")
delay = int(delay) if delay.strip() else defaultDelay

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--user-data-dir=C:\\Users\\Merri\\WebDriver') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
options.add_argument('--profile-directory=' + phonenumber)
options.add_argument('--profiling-flush=10000')
options.add_argument('--enable-aggressive-domstorage-flushing')
options.add_argument('--unexpectedAlertBehaviour')

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)
wait = WDWait(driver, delay)

print(f"""Количество номеров: {len(numbers)}""")
with open("Log/results.txt", "a") as file:
    file.write(f"Старт рассылки: {datetime.now()}\n")
encoded_string = urllib.parse.quote(msg)

i = 0
send = [] #успешно отправлено
abort =[] #ошибка отправки
unreg = [] #незарегистрированные номера

for number in numbers:
    try:
        i = i + 1
        
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_string}"
        driver.get(url)
        
        modal = wait.until(EC.visibility_of_element_located((By.XPATH, modal_elem)))
        modal_text = modal.text
        print(f'Текст модального окна:\n{modal_text}')

        if modal_text == 'Начало чата':
            pass
        
        if modal_text == 'Номер телефона, отправленный по ссылке, недействительный.':
            driver.find_element(By.XPATH, modal_btn).click()
            print(f"{i}. Номер {number} не зарегистрирован в WhatsApp")
            with open("Log/results.txt", "a") as file:
                file.write(f"{i}. Номер {number} не зарегистрирован в WhatsApp\n")
            unreg.append(number)
            sleep(random.uniform(1,2))
            continue
        
        wait.until(EC.element_to_be_clickable((By.XPATH, send_btn)))
        driver.find_element(By.XPATH, send_btn).click()
        
        print(f"{i}. Сообщение на номер {number} отправлено")
        with open("Log/results.txt", "a") as file:
            file.write(f"{i}. Сообщение на номер {number} отправлено\n")
        send.append(number)
        sleep(random.uniform(2,3))

    except NoSuchElementException:
        print(f"Элемент для номера {number} не найден, пропуск.")
        abort.append(number)
        sleep(random.uniform(2,5))
        continue

    except TimeoutException:
        print(f"Превышено время ожидания для номера {number}, пропуск.")
        abort.append(number)
        sleep(random.uniform(3,5))
        continue
    
    except UnexpectedAlertPresentException:
        # Обработка всплывающего окна
        print(f"Всплывающее окно для номера {number}, пропуск.")
        abort.append(number)
        sleep(random.uniform(2,5))
        continue

print(f'Отправлено: {len(send)}')
print(f'Ошибки отправки: {len(abort)}, {abort}')
print(f'Незаригистрированные номера: {len(unreg)}, {unreg}')
with open("Log/results.txt", "a") as file:
    file.write(f"{abort}\n{unreg}\n")

#/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[1]
#//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]
#//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button