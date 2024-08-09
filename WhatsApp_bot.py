from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import argparse
from datetime import datetime


# Константы для Selenium
# Constants for Selenium
url = f"https://web.whatsapp.com/"
xpath = "//button[@data-testid='compose-btn-send']"
xpathAttach = "//div[@data-testid='conversation-clip']"
cssIdOfDocument = "[aria-label='Документ']"
cssIdOfSendButton = "[aria-label='Отправить']"
xpathSearchField = "//div[@data-testid='chat-list-search']"
xpathFoundItem = "//span[contains(@class,'matched-text')]"
xpathInputLineForText = "//div[@data-testid='conversation-compose-box-input']"
xpathMessage = "//div[@role = 'row']"
xpathAuthorTime = "span[contains(@class,'_3FuDI')]"
xpathText1 = "span[contains(@class,'selectable-text')]"
xpathText2 = "span[contains(@class,'copyable-text')]"

commandEnableOrDisableJavaScript = "Emulation.setScriptExecutionDisabled"

# Константы для обработки сообщений
# Constants for message process
messageIsOutgoing = "message-out"
messageIsText = "data-pre-plain-text"
messageClassOfBody = "selectable-text copyable-text"
messageBodyStart = "<span>"
messageBodyStop = "</span>"
messageIsPicture = "img"
messageWarrningAboutPicture = "Смайлики не обрабатываю!  I don't process emoticons !"
fileNameWithLastMessage = "lastmessage.txt"

phonenumber = input('Введите номер от имени которого нужна рассылка: ')

class whatapp():
    """ Это класс бота для Whatsapp
       This class is bot for Whatsapp"""


    def startBrowser(self):
        options = webdriver.ChromeOptions()
# если у вас другой браузер, например FireFox, мы просто пишем options = webdriver.FirefoxOptions() .
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
# УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ python ФАЙЛ. Советую создать отдельную папку для него
        options.add_argument('--user-data-dir=C:\\Users\\Merri\\WebDriver') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
        options.add_argument('--profile-directory=' + phonenumber)
        options.add_argument('--profiling-flush=10000')
        options.add_argument('--enable-aggressive-domstorage-flushing')

# эти опции нужны чтобы подавить любые сообщения об ошибках  SSL, сертификатов и т.п. Но работает только последняя :(
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('log-level=3')
# INFO = 0,
# WARNING = 1,
# LOG_ERROR = 2,
# LOG_FATAL = 3.
# default is 0.
# Мы запускаем браузер
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# ждём его загрузки
        wait = WebDriverWait(self.driver, 30)
# идём туда
        self.driver.get(url)
# ждём загрузки страницы Whatsapp
        wait.until(EC.element_to_be_clickable((By.XPATH, xpathSearchField)))


    def finish(self):
# закрыть все
        self.driver.quit()

    def searchGroup(self, group_name):
# Найти группу для обработки
# В поле поиска вводим название группы и нажимаем на кнопку "Искать"
        self.driver.find_element(By.XPATH, xpathSearchField).send_keys(group_name)
        self.driver.find_element(By.XPATH, xpathFoundItem).click()
        sleep(5)


    def sendMessage(self, message):
# Разрешаем JavaSctipt
        self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': False})
# Ищем строку ввода и отправляем туда текст сообщения
        self.driver.find_element(By.XPATH, xpathInputLineForText).send_keys(message)
# теперь ищем кнопку "Отправить" и нажимаем на нее
        self.driver.find_element(By.XPATH, xpath).click()
        sleep(5)


    def searchLastMessageAndProcessMessages(self, dt):
# Запрещаем JavaSctipt
        self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': True})
# Выберем все сообщения
        messages = self.driver.find_elements(By.XPATH, xpathMessage)
        print(str(dt) + '. I found %s messages' % len(messages))
# Получим последнеe обработанное сообщение из файла
        f = open(fileNameWithLastMessage, "r")
        last_message = f.read()
        f.close()
        need_process = False
# просмотрим все сообщения
        for item in messages:
# получим тело сообщения
            line = str(item.get_attribute('innerHTML'))
# это исходящее сообщение. пропускаем
            if (messageIsOutgoing in line):
                 continue
# в сообщении нет текста. пропускаем
            if not (messageIsText in line):
                 continue
# извлечем дату, время и автора сообщения
            index1 = line.index(messageIsText)
            index2 = line.index("]", index1 + len(messageIsText))
            index3 = line.index(":", index2)
            author_datetime = line[index1 + len(messageIsText) + 2 : index3]
# извлечем текст сообщения
            index1 = line.index(messageClassOfBody)
            index2 = line.index(messageBodyStart, index1 + len(messageClassOfBody))
            index3 = line.index(messageBodyStop, index2)
            message = line[index2 + len(messageBodyStart): index3]
# сформируем полное сообщение для сравнения с последним обработанным
            full_message = author_datetime + " " + message
# если сообшение последнее обработанное, то начинаем обработку, пропустив это
            if (full_message == last_message):
                need_process = True
                continue
# обработка сообщений. Посылаем "эхо"
            if need_process:
# не будем отвечать на сообщения со смайликами
                if (messageIsPicture in message):  ## smile
                    message = messageWarrningAboutPicture
                self.sendMessage("Echo: " + message)
# Запрещаем JavaSctipt
                self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': True})
# запишем последнее обработанное сообщение
        if not (author_datetime is None):
            f = open(fileNameWithLastMessage, "w")
            f.write(full_message)
            f.close()
# Разрешаем JavaSctipt
        self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': False})


def main(args):
# основной бесконечный цикл. Прервать его - Ctrl+C
    try:
        while True:
            wa = whatapp()
            wa.startBrowser()
            wa.searchGroup(args.group)
            dt = datetime.now()
            wa.searchLastMessageAndProcessMessages(dt);
            wa.finish()
    except KeyboardInterrupt:
        wa.finish()
    return


if __name__ == '__main__':
# мы разбираем параметры командной строки
    parser = argparse.ArgumentParser(description='Process messages by Whatsapp')
    parser.add_argument('--group', help='Text for send', required=True)
    args = parser.parse_args()
# начать обработку
    main(args)