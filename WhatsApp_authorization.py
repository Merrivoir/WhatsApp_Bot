#Скрипт для первичной привязки whatsapp

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pyautogui

waElement = '/html/body/div[1]/div/div/div[2]/div[3]/header/header/div/div[1]'
waClass = 'x1iyjqo2 x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1rg5ohu _ao3e'
waInput = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
waSendButton = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button'

phonenumber = input('Введите номер для которого привязывается устройство (с кодом страны без плюса в начале): ')

options = webdriver.ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--user-data-dir=C:\\MEGA\\profiles\\chrome') # УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ ФАЙЛ. Советую создать отдельную папку.
options.add_argument('--profile-directory=' + phonenumber) #номер телефона для которого проходит авторизация
options.add_argument('--profiling-flush=10000')
options.add_argument('--enable-aggressive-domstorage-flushing')

driver = webdriver.Chrome(options=options)

url = "https://web.whatsapp.com/"
driver.get(url)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, waElement)))
sleep(3)
elements = driver.find_elements(By.CSS_SELECTOR, ".x1iyjqo2.x6ikm8r.x10wlt62.x1n2onr6.xlyipyv.xuxw1ft.x1rg5ohu._ao3e")

# Явное ожидание элемента, чтобы он был кликабельным
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, f'[title="Ольга Львова"]'))
)

# Кликаем по элементу
element.click()
sleep(3)
placeHolder = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, waInput))
)
placeHolder.send_keys("Hello world!")
sleep(1)
sendButton = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, waSendButton))
)
sendButton.click()
sleep(200)