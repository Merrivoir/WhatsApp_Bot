from selenium.webdriver.common.by import By

def extract_text(driver):
    try:
        # Находим сообщения в чате
        rows = driver.find_elements(By.XPATH, '//div[@role="row"]')
        last_row = rows[-1]  # Получаем последнее сообщение

        # Ищем все сообщения внутри элемента чата
        message = last_row.find_element(By.CSS_SELECTOR, 'div._akbu')
        message
        print(f"Сообщение: {message.text}")

    except Exception as e:
        print(f"Ошибка при извлечении текста: {e}")
