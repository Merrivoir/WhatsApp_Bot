from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep
import pyperclip
import random

waXPInputArea = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]"   #поле для ввода сообщения
waXPButton = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button"          #кнопка отправки сообщения
number = "РассылПавел"  #чат, в котором обрабатываются сообщения
unregistered = []
unsended = []

message = f"""✈️ Ты любишь путешествовать, но расходы всегда высокие? Мы знаем, как это исправить! 💸
🌍 Присоединяйся к нашему закрытому чату и узнай, как путешествовать за небольшие деньги, получая максимум удовольствия!

Для тех, кто хочет ещё и заработать на путешествиях – у нас есть особое предложение.
https://chat.whatsapp.com/BXfnpMNOHoW5vF8xg614eO

Если ссылка неактивна, просто напиши “ОК”, и сразу переходи по активной ссылке в чат. Мы тебя ждём!"""

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\MEGA\\profiles\\firefox\\77002990331')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

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
ttc = pyperclip.copy(message)

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
        sleep(2)
        
        try:
            # Ожидаем появление всплывающего окна с телефоном
            phone_popup = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "_ak4w")))
            phone_text_elements = phone_popup.find_elements(By.XPATH, ".//li//div[contains(@aria-label, 'Чат с')]")
            
            if phone_text_elements:

                phone_number = "+" + phone_text_elements[0].text.split("+")[-1]
                print(f"Номер {phone_number} зарегистрирован")
                phone_text_elements[0].click()
                
                sleep(random.uniform(1,1.8))

                try:
                        
                        inputArea = driver.find_element(By.XPATH, waXPInputArea)

                        sleep(random.uniform(0.4,1))
                        inputArea.send_keys(Keys.CONTROL, "v")

                        sleep(random.uniform(0.3,0.7))
                        driver.find_element(By.XPATH, waXPButton).click()

                        print(f"{i}. Сообщение на номер {phone_number} отправлено")
                        sleep(random.uniform(0.5,0.9))


                except Exception as e:
                        
                        unsended.append(phone_number)
                        print(f"{i}. Не удалось отправить сообщение на {phone_number}", e)
                        sleep(10)
                        element.click()

                sleep(random.uniform(1,2))
                    
                # Возвращаемся в исходный чат
                element.click()
                sleep(random.uniform(0.2,0.7))

            else:
                unregistered.append(link.text)
                print(f"{i}. Номер {link.text} не зарегистрирован")

                sleep(random.uniform(0.2,0.6))
                element.click()
        except TimeoutException:
            print("Всплывающее окно с телефоном не найдено.")
        
        i += 1  # Переход к следующему элементу, если успешно обработан

    except StaleElementReferenceException:
        print("Обновление элементов из-за StaleElementReferenceException...")
        sleep(2)  # Пауза перед повторной попыткой

    except Exception as e:
        print(f"{i}. Ошибка: {e}")
        sleep(10)
print(f"Незарегистрированные номера:\n{unregistered}")
print(f"Неотправленные номера:\n{unsended}")
#driver.quit()