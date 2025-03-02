from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from pyvirtualdisplay import Display

# Запуск виртуального дисплея
display = Display(visible=0, size=(1920, 1080))
display.start()

service = Service(log_path="geckodriver.log")

# Настройка Firefox в режиме headless
options = Options()
options.add_argument("--headless")  # Включение headless режима
options.add_argument("--disable-gpu")  # Отключение GPU
options.add_argument("--no-sandbox")  # Отключение sandbox (важно для контейнеров)
options.add_argument("--disable-dev-shm-usage")  # Использование /tmp вместо /dev/shm
options.set_capability("pageLoadStrategy", "eager")  # Ускоряет загрузку страницы

try:
    # Запуск браузера
    driver = webdriver.Firefox(service=service, options=options) #driver = webdriver.Firefox(service=service, options=options)

    # Тестовый запрос
    driver.get("https://www.google.com")
    print(f"Заголовок страницы: {driver.title}")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Закрытие браузера
    if 'driver' in locals():
        driver.quit()