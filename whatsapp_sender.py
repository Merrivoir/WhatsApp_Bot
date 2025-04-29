import sys
import os
import csv
import json
import random
import time
from datetime import datetime

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style, init

# Инициализация цветного вывода
init(autoreset=True)

# === Пути ===
CONTACTS_FILE = 'contacts/contacts.csv'
TEMPLATES_FILE = 'templates/templates.txt'
SUCCESS_LOG = 'logs/log_success.txt'
ERROR_LOG = 'logs/log_error.txt'
REPORT_FILE = 'logs/report.txt'
CONFIG_FILE = 'config.json'

# === Функции ===

import random

# Списки для живости сообщений
greetings = [
    "Здравствуйте, {name}.",
    "Добрый день, {name}.",
    "{name}, здарствуйте!",
]

good_endings = [
    "Хорошего дня! 🌟",
    "Буду рад помочь! 🙌",
    "Успехов и отличного настроения!",
    "Если что — пишите!",
]

def generate_message(name, templates):
    """Генерация живого сообщения для контакта."""
    # Выбираем случайный шаблон
    base_message = random.choice(templates)
    base_message = base_message.replace("{name}", name)

    parts = []

    # 80% шанс добавить приветствие
    if random.random() < 0.8:
        greet = random.choice(greetings).replace("{name}", name)
        parts.append(greet)

    # Добавляем основное сообщение
    parts.append(base_message)

    # 70% шанс добавить добрую фразу
    if random.random() < 0.7:
        ending = random.choice(good_endings)
        parts.append(ending)

    # Склеиваем всё через перенос строки
    final_message = "\n".join(parts)
    return final_message

def ensure_directories():
    """Создает необходимые папки и файлы при первом запуске."""
    for folder in ['contacts', 'templates', 'logs']:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
            f.write('name,phone\n')

    if not os.path.exists(TEMPLATES_FILE):
        with open(TEMPLATES_FILE, 'w', encoding='utf-8') as f:
            f.write('Привет, {name}!\n')

    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "minDelay": 7,
            "maxDelay": 20,
            "dailyLimit": 100
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)

    # Создаем CSV логи
    for csv_file, headers in [
        (SUCCESS_LOG.replace('.txt', '.csv'), ['name', 'phone', 'message', 'timestamp']),
        (ERROR_LOG.replace('.txt', '.csv'), ['name', 'phone', 'error', 'timestamp']),
        ('logs/not_registered.csv', ['name', 'phone', 'timestamp'])
    ]:
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)


def load_contacts():
    contacts = []
    with open(CONTACTS_FILE, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append({'name': row['name'], 'phone': row['phone']})
    return contacts

def load_sent_contacts():
    """Загружает уже отправленные контакты, чтобы не отправлять повторно."""
    sent_contacts = set()
    csv_file = SUCCESS_LOG.replace('.txt', '.csv')
    if os.path.exists(csv_file):
        with open(csv_file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sent_contacts.add(row['phone'])
    return sent_contacts

def load_templates():
    with open(TEMPLATES_FILE, encoding='utf-8') as f:
        templates = [line.strip() for line in f if line.strip()]
    return templates

def load_config():
    with open(CONFIG_FILE, encoding='utf-8') as f:
        return json.load(f)

def log_to_file(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now()} - {text}\n")

def log_to_csv(file_path, row):
    """Записывает одну строку в CSV лог."""
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(row)

def random_human_delay(min_sec, max_sec):
    delay = random.uniform(min_sec, max_sec)
    print(f"⏳ Ожидание {delay:.2f} секунд...")
    time.sleep(delay)

def slight_mouse_move():
    x, y = pyautogui.position()
    pyautogui.moveTo(x + random.randint(-20, 20), y + random.randint(-20, 20), duration=0.5)

def check_number_validity(driver):
    """Проверка, зарегистрирован ли номер в WhatsApp."""
    try:
        error_element = driver.find_element(By.XPATH, '//div[contains(@data-testid, "alert")]')
        if "номер не зарегистрирован" in error_element.text.lower():
            return False
    except:
        pass
    return True

def send_message(driver, phone, message):
    """Отправляет сообщение через WhatsApp Web."""
    url = f"https://web.whatsapp.com/send?phone={phone}&text={message}"
    driver.get(url)
    time.sleep(10)  # ждем загрузку чата

    slight_mouse_move()

    if not check_number_validity(driver):
        return 'not_registered'

    try:
        send_button = driver.find_element(By.XPATH, '//span[@data-icon="wds-ic-send-filled"]')
        send_button.click()
        return 'success'
    except Exception as e:
        print(f"⚠️ Ошибка при отправке: {e}")
        return 'error'
    

def print_status(message, color=Fore.WHITE):
    print(color + message + Style.RESET_ALL)

# === Основной скрипт ===

def main():
    ensure_directories()
    config = load_config()

    min_delay = config.get('minDelay', 7)
    max_delay = config.get('maxDelay', 20)
    daily_limit = config.get('dailyLimit', 100)

    contacts = load_contacts()
    templates = load_templates()
    sent_contacts = load_sent_contacts()

    # Фильтрация контактов
    contacts_to_send = [c for c in contacts if c['phone'] not in sent_contacts]

    if not contacts_to_send:
        print(Fore.YELLOW + "⚠️ Нет новых контактов для рассылки.")
        return

    print(Fore.CYAN + f"Найдено {len(contacts_to_send)} новых контактов для рассылки.")

    profile_path = r'C:\Users\Paul Lvov\AppData\Roaming\Mozilla\Firefox\Profiles\qa82eqx1.default'
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument('-profile')
    options.add_argument(profile_path)

    driver = webdriver.Firefox(options=options)

    driver.get('https://web.whatsapp.com/')

    print(Fore.CYAN + "🔎 Проверяю, залогинены ли вы в WhatsApp...")

    try:
        chat_list_xpath = '//div[@id="pane-side"]'
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, chat_list_xpath)))
        print(Fore.GREEN + "✅ Вы вошли в WhatsApp! Начинаем рассылку...")
    except Exception as e:
        print(Fore.RED + "❌ Не удалось войти в WhatsApp за 2 минуты.")
        driver.quit()
        sys.exit()

    sent_count = 0

    for contact in contacts_to_send:
        if sent_count >= daily_limit:
            print(Fore.YELLOW + f"⚠️ Достигнут дневной лимит в {daily_limit} сообщений.")
            break

        name = contact['name']
        phone = contact['phone']
        message = generate_message(name, templates)

        print_status(f"📨 Отправка сообщения для {name} ({phone})...", Fore.BLUE)
        result = send_message(driver, phone, message)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if result == 'success':
            log_to_csv(SUCCESS_LOG.replace('.txt', '.csv'), [name, phone, message, timestamp])
            print_status(f"✅ Успешно отправлено {name}", Fore.GREEN)
        elif result == 'not_registered':
            log_to_csv('logs/not_registered.csv', [name, phone, timestamp])
            print_status(f"⚠️ {name} не зарегистрирован в WhatsApp", Fore.YELLOW)
        else:
            log_to_csv(ERROR_LOG.replace('.txt', '.csv'), [name, phone, "Ошибка отправки", timestamp])
            print_status(f"❌ Ошибка отправки {name}", Fore.RED)

        sent_count += 1
        random_human_delay(min_delay, max_delay)

    print(Fore.CYAN + "\n📋 Работа завершена.")
    driver.quit()


if __name__ == "__main__":
    main()
