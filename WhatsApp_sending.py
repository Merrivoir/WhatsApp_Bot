from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from time import sleep
import urllib.parse
import random

#блок импорта номеров и сообщений
from Aiqerim import leads3_aq as numbers
from Aiqerim import message_aq as message

#Элементы на странице
modal_elem = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
modal_btn = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button'
send_btn = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'

phonenumber = input('Введите номер от имени которого нужна рассылка: ')

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
wait = WebDriverWait(driver, 30)

nm_test = ["+77777777777", "+77474728450"]
encoded_string = urllib.parse.quote(message)

i = 0
send = [] #успешно отправлено
abort =[] #ошибка отправки
unreg = [] #незарегистрированные номера

for number in nm_test:
    try:
        i = i + 1
        
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_string}"
        driver.get(url)
        
        modal = wait.until(EC.visibility_of_element_located((By.XPATH, modal_elem)))
        modal_text = modal.text
        
        if modal_text == 'Номер телефона, отправленный по ссылке, недействительный.':
            driver.find_element(By.XPATH, modal_btn).click()
            print(f"{i}. Номер {number} не зарегистрирован в WhatsApp")
            unreg.append(number)
            sleep(random.uniform(1,2))
            continue

        wait.until(EC.element_to_be_clickable((By.XPATH, send_btn)))
        driver.find_element(By.XPATH, send_btn).click()
        
        print(f"{i}. Сообщение на номер {number} отправлено")
        send.append(number)
        sleep(random.uniform(1,2))

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
print(f'Ошибки отправки: {len(abort)}')
print(f'Незаригистрированные номера: {len(unreg)}')

#/html/body/div[1]/div/div/span[2]/div/span/div/div/div/div/div/div[1]
#//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]
#//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button