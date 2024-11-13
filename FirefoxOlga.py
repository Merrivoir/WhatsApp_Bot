from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep
from datetime import datetime, timedelta
import pyperclip
import random
from CashFlow_chain import ColdBaseMsg as msg

print(f"----------------------------------------------------------------------------")
print(f"Скрипт FirefoxOlga начал работу")

number = "Муж"  #чат, в котором обрабатываются сообщения
modal = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]'
unregistered = []
unsended = []

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox\\77058893755')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

try:
    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Чаты']")))
    print("Клиент запущен, чаты обнаружены")

except Exception as e:
    print(f"""Клиент не запущен
          Ошибка {e}""")

element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="{number}"]')))
element.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, f"//span[@dir='auto' and @style='min-height: 0px;' and contains(@class, '_ao3e') and text()='{number}']")
    )
)

lastMessage = driver.find_elements(By.CSS_SELECTOR, f'[role="row"]')[-1]
links = lastMessage.find_elements(By.XPATH, "//a[@dir='auto' and @style='cursor: pointer;' and contains(@class, '_ao3e selectable-text copyable-text')]")
print(f"Количество номеров в списке: {len(links)}")

i = 0

while True:
    try:
        lastMessage = driver.find_elements(By.CSS_SELECTOR, f'[role="row"]')[-1]
        links = lastMessage.find_elements(By.XPATH, "//a[@dir='auto' and @style='cursor: pointer;' and contains(@class, '_ao3e selectable-text copyable-text')]")
        
        if i == len(links):
            print(f"Обработка номеров завершена")
            break
        
        link = links[i]     # Переход к нужной ссылке
        link.click()
        sleep(2)
        
        try:            
            wait = WebDriverWait(driver, 10)
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//span[contains(text(), "Проверка номера телефона...")]'))) # Ждем, пока элемент с указанным текстом не исчезнет
            phone_text_elements = driver.find_elements(By.XPATH, ".//li//div[contains(@aria-label, 'Чат с')]") # Ожидаем появление всплывающего окна с телефоном
            
            if phone_text_elements:
                phone_number = "+" + phone_text_elements[0].text.split("+")[-1]
                print(f"{i}. Номер {phone_number} зарегистрирован")
                phone_text_elements[0].click()
                
                sleep(random.uniform(1,1.8))
                WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, modal)))

                try:                        
                    inputArea = driver.find_element(By.CSS_SELECTOR, 'div[aria-placeholder="Введите сообщение"]')

                    sleep(random.uniform(0.4,1))

                    ttc = random.choice(msg)
                    pyperclip.copy(ttc)

                    sleep(random.uniform(2.1, 3.6))
                    inputArea.send_keys(Keys.CONTROL, "v")

                    sleep(random.uniform(1.3,2.7))
                    driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Отправить"]').click()

                    print(f"""{i}. Сообщение №{msg.index(ttc)} на номер {phone_number} отправлено - {datetime.now()}""")
                    sleep(random.uniform(0.5,0.9))

                except Exception as e:                        
                    unsended.append(phone_number)
                    print(f"{i}. Не удалось отправить сообщение на {phone_number}", e)
                    sleep(20)
                    element.click()

                nextMessage = random.uniform(900.0,1700.17)
                future_datetime = datetime.now() + timedelta(seconds=nextMessage)
                print(f"Следующее сообщение через: {nextMessage}, в {future_datetime}")
                sleep(nextMessage)
                    
                element.click()             # Возвращаемся в исходный чат
                
            else:
                unregistered.append(link.text)
                print(f"{i}. Номер {link.text} не зарегистрирован")

                sleep(random.uniform(0.2,0.6))
                element.click()

        except TimeoutException:            
            unsended.append(link.text)
            print("Всплывающее окно с телефоном не найдено.")
        
        i += 1  # Переход к следующему элементу, если успешно обработан

    except StaleElementReferenceException:
        print("Обновление элементов из-за StaleElementReferenceException...")
        sleep(20)  # Пауза перед повторной попыткой

    except Exception as e:
        print(f"{i}. Ошибка: {e}")
        sleep(5)
        element.click()

print(f"Незарегистрированные номера:\n{unregistered}")
print(f"Неотправленные номера:\n{unsended}")
print(f"----------------------------------------------------------------------------")
#driver.quit()