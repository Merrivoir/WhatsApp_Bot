from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep
from datetime import datetime
import urllib.parse
import random

waXPInputArea = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]"
waXPButton = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button"
number = "+7 747 472 8450"
message = f"""Путешествуй по всему миру, не тратя огромные деньги! ✈️🌍
💼 Хочешь узнать, как экономить на каждом туре и при этом создавать авторские туры для других?

Вступай в наш чат и узнай секреты, как сделать путешествия доступными и выгодными.
https://chat.whatsapp.com/BXfnpMNOHoW5vF8xg614eO

Если ссылка не работает, просто ответь “ОК”, и сразу переходи по активной ссылке в чат. Мы тебя ждём!"""

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox\\77757468937')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

element = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="{number}"]'))
)
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
        # Переопределяем `lastMessage` и `links` на каждой итерации
        lastMessage = driver.find_elements(By.CSS_SELECTOR, f'[role="row"]')[-1]
        links = lastMessage.find_elements(By.XPATH, "//a[@dir='auto' and @style='cursor: pointer;' and contains(@class, '_ao3e selectable-text copyable-text')]")
        
        if i == len(links):
            print(f"Обработка номеров завершена")
            break
        
        link = links[i]     # Переход к нужной ссылке
        link.click()
        sleep(1)
        try:
            # Ожидаем появление всплывающего окна с телефоном
            phone_popup = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "_ak4w"))
            )
            phone_text_elements = phone_popup.find_elements(By.XPATH, ".//li//div[contains(@aria-label, 'Чат с')]")
            
            if phone_text_elements:
                phone_number = "+" + phone_text_elements[0].text.split("+")[-1]
                print(f"Номер {phone_number} зарегистрирован")
                phone_text_elements[0].click()
                
                sleep(random.uniform(1,2))

                try:
                        inputArea = driver.find_element(By.XPATH, waXPInputArea)
                        for char in message:
                            inputArea.send_keys(char)
                            sleep(0.03)

                        sleep(random.uniform(0.2,1))
                        driver.find_element(By.XPATH, waXPButton).click()
                        print(f"Сообщение на номер {phone_number} отправлено")
                except Exception as e:
                        print(f"Не удалось отправить сообщение на {phone_number}", e)

                sleep(random.uniform(1,2))
                    
                # Возвращаемся в исходный чат
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="{number}"]'))
                    )
                element.click()
                sleep(1)
            else:
                print(f"Номер {link.text} не зарегистрирован")
                element.click()
        except TimeoutException:
            print("Всплывающее окно с телефоном не найдено.")
        
        i += 1  # Переход к следующему элементу, если успешно обработан

    except StaleElementReferenceException:
        print("Обновление элементов из-за StaleElementReferenceException...")
        sleep(2)  # Пауза перед повторной попыткой

    except Exception as e:
        print(f"Ошибка: {e}")
driver.quit()