from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.get("https://www.google.com")
print(f"Заголовок страницы: {driver.title}")
driver.quit()