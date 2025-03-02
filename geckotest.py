from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com")
print("Заголовок страницы:", driver.title)
driver.quit()
