from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep
from datetime import datetime

options =  webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\Msync\\profiles\\firefox\\8450')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"
driver.get(url)

WebDriverWait(driver, 300).until( EC.presence_of_element_located((By.XPATH, '//h1[contains(@class, "x1qlqyl8") and text()="Чаты"]')) )
print("Чаты загружены") # Ожидание появления заголовка "Чаты" (как маркер завершения загрузки страницы)

def unreadMsg(driver):
    try: # Находим все элементы, соответствующие данным условиям
        elements = driver.find_elements(By.XPATH, '//div[contains(@class, "x10l6tqk xh8yej3 x1g42fcv")]')
        for element in elements:
            try: # Проверка наличия элемента с aria-label="Непрочитанные"
                title_element = element.find_element(By.CSS_SELECTOR, 'span[title]')
                unread = element.find_element(By.XPATH, './/span[contains(translate(@aria-label, "НЕПРОЧИТАН", "непрочитан"), "непрочитан")]')
                # Если элемент найден, извлекаем текст из другого элемента внутри того же контейнера
                print(f"Непрочитанное сообщение от: {title_element.get_attribute('title')}")
            except Exception as e: # Если элемент с aria-label="Непрочитанные" не найден
                pass
    except Exception as e: print(f"Ошибка: {e}")

while True:
    try:
        unreadMsg(driver)
        sleep(5)  # Пауза между проверками в 10 секунд
    except KeyboardInterrupt:
        driver.quit()