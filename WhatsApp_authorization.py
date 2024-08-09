#Скрипт для первичной привязки whatsapp

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

phonenumber = input('Введите номер для которого привязывается устройство (с кодом страны без плюса в начале): ')

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--user-data-dir=C:\\Users\\Merri\\WebDriver') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
options.add_argument('--profile-directory=' + phonenumber) #номер телефона для которого проходит авторизация
options.add_argument('--profiling-flush=10000')
options.add_argument('--enable-aggressive-domstorage-flushing')

driver = webdriver.Chrome(options=options)

url = "https://web.whatsapp.com/"
driver.get(url)
sleep(60)