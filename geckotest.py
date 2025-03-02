from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True  # Только headless-режим, без лишних аргументов

try:
    driver = webdriver.Firefox(options=options)
    driver.get("https://www.google.com")
    print("Заголовок страницы:", driver.title)
except Exception as e:
    print("Ошибка:", e)
finally:
    if 'driver' in locals():
        driver.quit()
