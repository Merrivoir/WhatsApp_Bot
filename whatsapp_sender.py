import sys
import os
import csv
import json
import random
import time
import pyperclip
import pyautogui

from datetime import datetime
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
STOPLIST_FILE = 'contacts/stoplist.csv'

# === Функции ===

import random

# Списки для живости сообщений
greetings = [
    "Здравствуйте, {name}",
    "{name}, Здравствуйте",
]

good_endings = [
    "",
    "",
]

def generate_message(name, templates): 
    """Генерация живого сообщения для контакта с учетом отсутствия имени."""
    # Определяем, есть ли настоящее имя
    has_real_name = name.lower() != "здравствуйте"

    # Выбираем случайный шаблон
    base_message = random.choice(templates)
    base_message = base_message.replace("{name}", name) if has_real_name else base_message.replace("{name}", "")

    parts = []

    # Приветствие (с именем или без)
    if random.random() < 1:
        if has_real_name:
            greet = random.choice(greetings).replace("{name}", name)
        else:
            greet = "Здравствуйте!"
        parts.append(greet)

    # Основное сообщение
    parts.append("""
👋 Ранее вы интересовались игрой CashFlow, и у нас отличные новости — мы открыли группы для новичков! 🎉

📅 *Вторник с 19:00 до 22:00*
📅 *Воскресенье с 17:00 до 20:00*

✅ _Объясняем правила с нуля_
✅ _Поддерживаем на каждом этапе_
✅ _Помогаем увидеть свои точки роста_
✅ _Создаём тёплую атмосферу и знакомим с классными людьми_

Это отличная возможность начать путь к финансовой грамотности и новым возможностям в жизни и бизнесе.

*Чтобы записаться — просто напишите "+" в ответ на это сообщение*
Буду рада вас видеть на игре! """)

    # Завершение
    if random.random() < 1:
        parts.append(random.choice(good_endings))

    # Склеиваем с переносами строк
    final_message = "\n".join(part for part in parts if part.strip())
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


def load_stoplist(filepath=STOPLIST_FILE):
    """Загружает номера из стоп-листа."""
    stop_numbers = set()
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            phone = line.strip()
            if phone:
                stop_numbers.add(phone)
    print(f"📛 Загружено {len(stop_numbers)} номеров из стоп-листа")
    return stop_numbers


def load_contacts(filepath=CONTACTS_FILE, stoplist_path=STOPLIST_FILE):
    """Загружает контакты и исключает номера из стоп-листа."""
    stop_numbers = load_stoplist(stoplist_path)
    all_contacts = []
    filtered_contacts = []

    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            phone = row.get('phone', '').strip()
            if not phone:
                continue

            raw_name = row.get('name', '').strip()
            name = raw_name.split()[0] if raw_name else "Здравствуйте"

            all_contacts.append({'name': name, 'phone': phone})

            if phone not in stop_numbers:
                filtered_contacts.append({'name': name, 'phone': phone})

    print(f"📄 Всего контактов в CSV: {len(all_contacts)}")
    print(f"🚫 Из них в стоп-листе: {len(all_contacts) - len(filtered_contacts)}")
    print(f"✅ Допущено к рассылке: {len(filtered_contacts)}")

    return filtered_contacts


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
    url = f"https://web.whatsapp.com/send?phone={phone}"
    print(f"📨 Открываем чат с номером: {phone}")
    driver.get(url)
    time.sleep(20)  # ждем загрузку чата

    slight_mouse_move()
    print("🖱️ Немного подвинули мышку")

    if not check_number_validity(driver):
        print("❌ Номер не зарегистрирован в WhatsApp")
        return 'not_registered'

    try:
        print("📋 Копируем сообщение в буфер обмена...")
        pyperclip.copy(message)
        time.sleep(0.2)
        copied = pyperclip.paste()
        if copied != message:
            print("❌ Ошибка: сообщение не попало в буфер обмена!")
            return 'clipboard_error'
        print("📋 Сообщение в буфере подтверждено")

        print("⌛ Ожидаем появление поля ввода сообщения...")
        input_box = WebDriverWait(driver, 30).until(
            lambda d: d.find_element(By.XPATH, '//div[@aria-placeholder="Введите сообщение"]')
        )
        print("✅ Поле ввода найдено. Кликаем...")
        input_box.click()

        # Обязательно активируем элемент на всякий случай
        driver.execute_script("arguments[0].focus();", input_box)
        time.sleep(0.5)

        print("⌨️ Вставляем сообщение (Ctrl+V)...")
        input_box.send_keys(Keys.CONTROL, 'v')
        time.sleep(0.3)

        print("📤 Отправляем сообщение (Enter)...")
        input_box.send_keys(Keys.ENTER)
        print("✅ Сообщение отправлено")
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
