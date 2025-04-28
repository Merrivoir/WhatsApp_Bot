from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException, NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException, StaleElementReferenceException
from time import sleep

print(f"----------------------------------------------------------------------------")
print(f"Скрипт начал работу")

options = webdriver.FirefoxOptions()
options.add_argument('-profile')
options.add_argument('C:\\Msync\\profiles\\firefox\\77058893755')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/"

driver.get(url)
WebDriverWait(driver, 300).until( EC.presence_of_element_located((By.XPATH, '//h1[@class="x1qlqyl8 x1pd3egz xcgk4ki"]')) )
print(f"Браузер запущен")

class WhatsAppBot:

    def check_chats(self):
        try:
            # Находим все чаты
            chats = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            for chat in chats:
                # Узнаем title
                contact_title = chat.find_element(By.CSS_SELECTOR, 'span[title]').get_attribute('title')
                print(f"Контакт: {contact_title}")
                
                # Проверяем наличие непрочитанных сообщений
                unread_msgs = chat.find_elements(By.CSS_SELECTOR, 'span[aria-label*="непрочитанное сообщение"]')
                if unread_msgs:
                    num_unread = unread_msgs[0].get_attribute('aria-label')
                    print(f"Количество непрочитанных сообщений: {num_unread}")
                else:
                    print("Непрочитанных сообщений нет")
        except Exception as e:
            print("Ошибка при проверке чатов:", e)

    def run(self):
        try:
            while True:
                self.check_chats()
                sleep(10)  # Пауза между проверками в 10 секунд
        except KeyboardInterrupt:
            driver.quit()

if __name__ == '__main__':
    bot = WhatsAppBot()
    bot.run()