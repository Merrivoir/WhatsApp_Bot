from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep
from datetime import datetime
import pyperclip
import random
from Aiqerim import messagesTravorium

modal = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
number = "РассылПавел"  #чат, в котором обрабатываются сообщения
unregistered = []
unsended = []

options =  webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox\\77076261208')

driver = webdriver.Firefox(options=options)
tabs = driver.window_handles        # Переключаемся на нужную вкладку по индексу
print(tabs[0].title())
#driver.switch_to.window(tabs[0])    # Переход на первую вкладку

url = f"https://web.whatsapp.com/"
driver.get(url)
sleep(6)

element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="{number}"]')))
element.click()

print(f"Старт рассылки {datetime.now()}")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, f"//span[@dir='auto' and @style='min-height: 0px;' and contains(@class, '_ao3e') and text()='{number}']")
    )
)

lastMessage = driver.find_elements(By.CSS_SELECTOR, f'[role="row"]')[-1]
links = lastMessage.find_elements(By.XPATH, "//a[@dir='auto' and @style='cursor: pointer;' and contains(@class, '_ao3e selectable-text copyable-text')]")
print(f"Количество номеров в списке: {len(links)}")

i = 0
ttc = random.choice(messagesTravorium)
ind = messagesTravorium.index(ttc)
pyperclip.copy(ttc)

while True:
    try:
        pyperclip.copy(ttc)
        # Переопределяем `lastMessage` и `links` на каждой итерации
        lastMessage = driver.find_elements(By.CSS_SELECTOR, f'[role="row"]')[-1]
        links = lastMessage.find_elements(By.XPATH, "//a[@dir='auto' and @style='cursor: pointer;' and contains(@class, '_ao3e selectable-text copyable-text')]")
        
        if i == len(links):
            print(f"Обработка номеров завершена")
            break
        
        link = links[i]     # Переход к нужной ссылке
        link.click()
        sleep(2)
        
        try:
            
            wait = WebDriverWait(driver, 30)
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//span[contains(text(), "Проверка номера телефона...")]'))) # Ждем, пока элемент с указанным текстом не исчезнет
            phone_text_elements = driver.find_elements(By.XPATH, ".//li//div[contains(@aria-label, 'Чат с')]") # Ожидаем появление всплывающего окна с телефоном
            
            if phone_text_elements:

                phone_number = "+" + phone_text_elements[0].text.split("+")[-1]
                print(f"{i}. Номер {phone_number} зарегистрирован")
                phone_text_elements[0].click()
                
                sleep(random.uniform(2.2,2.8))
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, modal)))

                try:
                        #pyperclip.copy(ttc)
                        inputArea = driver.find_element(By.CSS_SELECTOR, 'div[aria-placeholder="Введите сообщение"]')

                        sleep(random.uniform(1.4,2.4))
                        inputArea.send_keys(Keys.CONTROL, "v")

                        sleep(random.uniform(1.1,1.7))
                        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Отправить"]').click()

                        with open("Log/AQ.txt", "a") as file:
                            file.write(f"Сообщение №{ind} на номер {phone_number} отправлено | {datetime.now()}\n")
                        
                        print(f"{i}. Сообщение №{ind} на номер {phone_number} отправлено")
                        sleep(random.uniform(1.5,2.9))

                except Exception as e:
                        
                        unsended.append(phone_number)
                        print(f"{i}. Не удалось отправить сообщение на {phone_number}", e)
                        sleep(5)
                        element.click()

                sleep(random.uniform(1,2))
                    
                # Возвращаемся в исходный чат
                element.click()
                sleep(random.uniform(1.1,1.7))

            else:
                unregistered.append(link.text)
                print(f"{i}. Номер {link.text} не зарегистрирован")
                sleep(random.uniform(0.7,1.6))
                element.click()

        except TimeoutException:
            unsended.append(link.text)
            print("Всплывающее окно с телефоном не найдено.")
        
        i += 1  # Переход к следующему элементу, если успешно обработан

    except StaleElementReferenceException:
        print("Обновление элементов из-за StaleElementReferenceException...")
        sleep(2)  # Пауза перед повторной попыткой

    except Exception as e:
        print(f"{i}. Ошибка: {e}")
        sleep(5)
        element = driver.find_element(By.CSS_SELECTOR, f'[title="{number}"]')
        element.click()

print(f"Незарегистрированные номера:\n{unregistered}")
print(f"Неотправленные номера:\n{unsended}")

with open("Log/AQUNR.txt", "a") as file:
    for log in unregistered:
        file.write(f"{log}\n")

print(f"Окончание рассылки {datetime.now()}")