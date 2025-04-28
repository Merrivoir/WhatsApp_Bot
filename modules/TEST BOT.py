import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

# Константы
BASE_URL = "https://web.whatsapp.com/"
LOG_FILE = "Log/whatsapp_bot_log.txt"
TIMEOUT = 30  # Время ожидания в секундах
TARGET_CONTACT_NAME = "+7 747 472 8450"  # Имя контакта, на сообщения которого бот будет реагировать
BOT_RESPONSE = "Спасибо за ваше сообщение! Я чат-бот. Как могу помочь?"  # Ответ бота
MAX_MESSAGE_AGE_MINUTES = 5  # Максимальный возраст сообщения для реакции (в минутах)

# Настройка логгера
def Logger(text):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {text}\n\n")

# Отправка сообщения
# Отправка сообщения
def send_message(driver, message):
    try:
        # Находим поле ввода текста
        input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        input_box.click()  # Активируем поле ввода
        input_box.clear()  # Очищаем поле (на случай, если там уже есть текст)

        # Вводим текст посимвольно
        for char in message:
            input_box.send_keys(char)
            time.sleep(0.02)  # Небольшая задержка между символами для надежности

        # Находим кнопку отправки сообщения
        send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
        send_button.click()

        print(f"Отправлено сообщение: {message}")
        Logger(f"Отправлено сообщение: {message}")
        return True

    except Exception as e:
        print("Ошибка при отправке сообщения:", e)
        Logger(f"Ошибка при отправке сообщения: {e}")
        return False

# Переход к чату с целевым контактом
def navigate_to_target_chat(driver, target_contact_name):
    try:
        # CSS-селектор для поиска чата по имени контакта
        chat_selector = f'span[title="{target_contact_name}"]'
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, chat_selector)))
        target_chat = driver.find_element(By.CSS_SELECTOR, chat_selector)
        target_chat.click()
        print(f"Перешли к чату с контактом: {target_contact_name}")
        Logger(f"Перешли к чату с контактом: {target_contact_name}")
        return True

    except TimeoutException:
        print(f"Чат с контактом '{target_contact_name}' не найден.")
        Logger(f"Чат с контактом '{target_contact_name}' не найден.")
        return False

# Проверка новых сообщений
def check_new_messages(driver):
    try:
        # Ищем все строки с сообщениями
        rows = driver.find_elements(By.XPATH, '//div[@role="row"]')
        if not rows:
            return None

        # Берем последнюю строку (последнее сообщение)
        last_row = rows[-1]

        # Проверяем, является ли сообщение входящим
        try:
            message_container = last_row.find_element(By.CSS_SELECTOR, 'div.message-in')
            is_incoming = True
        except NoSuchElementException:
            #print("Сообщение исходящее или не содержит класс message-in. Пропускаем.")
            return None

        # Извлекаем метаданные (время и отправитель)
        try:
            metadata = message_container.find_element(By.CSS_SELECTOR, 'div.copyable-text').get_attribute("data-pre-plain-text")
        except NoSuchElementException:
            metadata = "Метаданные не найдены"

        # Извлекаем текст сообщения
        try:
            text = message_container.find_element(By.CSS_SELECTOR, 'span._ao3e span').text.strip()
        except NoSuchElementException:
            text = "Текст не найден"

        # Извлекаем время отправки из метаданных
        try:
            timestamp = metadata.split(']')[0].strip('[')  # Извлекаем время из data-pre-plain-text
        except Exception:
            timestamp = "Время не найдено"

        return {
            "metadata": metadata.strip(),
            "text": text.strip(),
            "timestamp": timestamp.strip()
        }

    except (NoSuchElementException, StaleElementReferenceException):
        return None

# Проверка свежести сообщения
def is_message_fresh(timestamp):
    try:
        # Преобразуем время отправки в объект datetime
        message_time = datetime.strptime(timestamp, "%H:%M, %d.%m.%Y")
        current_time = datetime.now()

        # Вычисляем разницу во времени
        time_difference = current_time - message_time
        return time_difference <= timedelta(minutes=MAX_MESSAGE_AGE_MINUTES)

    except ValueError:
        print(f"Ошибка при обработке времени: {timestamp}")
        return False

# Главная функция
def main():
    print(f"----------------------------------------------------------------------------")
    print(f"Чат-бот начал работу - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Настройка браузера
    options = webdriver.FirefoxOptions()
    options.add_argument('-profile')
    options.add_argument('C:\\Msync\\FFP')

    print("Запуск браузера...")
    driver = webdriver.Firefox(options=options)
    driver.get(BASE_URL)

    try:
        # Ожидаем ручную авторизацию пользователя
        input("Пожалуйста, дождитесь загрузки чатов и нажмите Enter для продолжения...")

        # Переходим к чату с целевым контактом
        if not navigate_to_target_chat(driver, TARGET_CONTACT_NAME):
            print("Не удалось найти чат с указанным контактом. Завершение работы.")
            return

        # Бесконечный цикл для прослушивания новых сообщений
        last_processed_message = None
        while True:
            try:
                # Проверяем новое сообщение
                message_data = check_new_messages(driver)
                if message_data and message_data["text"] != last_processed_message:
                    print(f"Обнаружено новое сообщение:")
                    print(f"- Метаданные: {message_data['metadata']}")
                    print(f"- Текст: {message_data['text']}")
                    print(f"- Время: {message_data['timestamp']}")

                    # Проверяем свежесть сообщения
                    if is_message_fresh(message_data["timestamp"]):
                        print("Сообщение свежее. Отправляем ответ.")
                        send_message(driver, BOT_RESPONSE)
                        Logger(f"Обработано новое сообщение:\n{message_data}")
                    else:
                        print("Сообщение устарело. Пропускаем.")

                    # Обновляем последнее обработанное сообщение
                    last_processed_message = message_data["text"]

                # Ждем перед следующей проверкой
                time.sleep(MAX_MESSAGE_AGE_MINUTES)

            except KeyboardInterrupt:
                print("\nПрерывание работы скрипта (Ctrl+C). Завершаем работу...")
                break

    finally:
        print("Закрытие браузера...")
        driver.quit()

    print(f"----------------------------------------------------------------------------")
    print(f"Чат-бот завершил работу - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()