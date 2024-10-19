#//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button
sendButtonXP = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException, SessionNotCreatedException
from time import sleep
from datetime import datetime
import urllib.parse
import random

defaultDelay = 30
phonenumber = input("Введите номер от имени которого нужна рассылка: ")
delay = input(f"Введите значение задержки (по умолчанию {defaultDelay}): ")
delay = int(delay) if delay.strip() else defaultDelay

options = webdriver.FirefoxOptions()
options.add_argument('-new-instance')
options.add_argument('-profile')
options.add_argument('C:\\Users\\Merri\\testFire')

driver = webdriver.Firefox(options=options)

url = f"https://web.whatsapp.com/send?phone=77757468937&text=Selenium%20test"
driver.get(url)
sleep(5)
sendButton = driver.find_element(By.XPATH, sendButtonXP)
sendButton.click()
driver.quit()