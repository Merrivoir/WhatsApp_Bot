from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Указываем путь к chromedriver через Service
chrome_service = Service("C:/chromedriver/chromedriver.exe")

# Настройка опций для подключения к открытому экземпляру Chrome
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# Подключаемся к Chrome через WebDriver, передавая объект Service
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

tabs = driver.window_handles

for tab in tabs:
    driver.switch_to.window(tab)
    print("Вкладка URL:", driver.current_url)