import sys
import os
import csv
import json
import random
import time
import pyperclip
import pyautogui

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from colorama import Fore, Style, init

# Инициализация цветного вывода
init(autoreset=True)

# === Пути ===
CONTACTS_FILE = 'contacts/Base.csv'
TEMPLATES_FILE = 'templates/templates.txt'
SUCCESS_LOG = 'logs/log_success_2206.csv'
ERROR_LOG = 'logs/log_error.txt'
REPORT_FILE = 'logs/report.txt'
CONFIG_FILE = 'config.json'
STOPLIST_FILE = 'contacts/stoplist.csv'

# === Функции ===

import random

# Списки для живости сообщений
greetings = [
    "Здравствуйте, {name}",
    "{name}, здравствуйте",
    "{name}, добрый день"
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
    """ parts.append(
Это Ольга Львова — эксперт по инвестициям и основатель клуба CashFlow в Алматы.

Вы интересовались нашими играми, но пока не успели поучаствовать.
Поэтому хочу лично пригласить вас в обучение, которое поможет вам уверенно разобраться в личных финансах и инвестициях.

📌 Я создала практический онлайн-курс:
«Финансовая грамотность, инвестиции и крипта — понятным языком»

Он подойдёт даже тем, кто пока не разбирается в деньгах, не умеет инвестировать и не знает, с чего начать.

В программе:
— учёт и рост дохода
— как открыть брокерский счёт в Казахстане
— как покупать акции и крипту
— как собрать портфель и не потерять деньги
— бонус: как не попасть на мошенников и не сдаться на старте

🎁 Только сейчас — для первых 100 участников курс стоит 15 000 ₸
(вместо 25 000 ₸).

📲 Если хотите присоединиться — просто напишите в ответ «ХОЧУ КУРС», и я пришлю вам ссылку телеграм канал, где я уже опубликовала программу курса.

Это идеальное начало, если вы давно хотели разобраться в деньгах, но не знали, с чего начать.

Буду рада видеть вас в числе участников!
С уважением, Ольга Львова"""
    
    parts.append("""
Это Ольга Львова - ведущая игр CashFlow, эксперт по финансовой грамотности и инвестициям.

Вы уже были у нас на игре, а значит — знаете, насколько важно уметь управлять деньгами и принимать осознанные финансовые решения.

📣 Сейчас хочу лично пригласить вас на мой новый практический курс:
«Финансовая грамотность, инвестиции и крипта — для реальной жизни»

📌 В программе:
— учёт личных финансов, оптимизация и рост дохода
— как открыть брокерский счёт в Казахстане
— как собрать и управлять инвестиционным портфелем
— как безопасно начать с криптовалютой
— бонус: психология инвестора, как не попасть на мошенников, топ-5 ошибок новичков

🎁 Специальное предложение для первых 100 участников:
Вы можете пройти весь курс всего за 15 000 ₸
(дальше цена вырастет до 250 000 ₸)

Это ваш шанс за короткое время навести порядок в финансах, разобраться в инвестициях и выйти на новый уровень уверенности в деньгах.

📲 Подписывайтесь на канал https://t.me/+X5Hlfy7pQnoyZGMy, где вы сможете ознакомиться с программой курса

Буду рада видеть вас в числе участников!
""")

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

def wait_for_chat_modal(driver, timeout=180):
    modal_xpath = '//h1[text()="Начало чата"]/ancestor::div[@data-animate-modal-popup="true"]'
    start_time = time.time()

    try:
        print("⌛ Ожидаем появления модального окна 'Начало чата'...")
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, modal_xpath))
        )
        print("✅ Модальное окно появилось")

    except TimeoutException:
        print("⚠️ Модальное окно не появилось за отведённое время")
        return False
    except Exception as e:
        print(f"⚠️ Ошибка при ожидании появления модального окна: {e}")
        return False

    try:
        print("⌛ Ожидаем исчезновения модального окна...")
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, modal_xpath))
        )
        print(f"✅ Модальное окно исчезло через {round(time.time() - start_time, 2)} секунд")
        return True

    except TimeoutException:
        print("⚠️ Модальное окно не исчезло за отведённое время")
        return False
    except Exception as e:
        print(f"⚠️ Ошибка при ожидании исчезновения модального окна: {e}")
        return False


def send_message(driver, phone, message):
    """Отправляет сообщение через WhatsApp Web."""
    url = f"https://web.whatsapp.com/send?phone={phone}"
    print(f"📨 Открываем чат с номером: {phone}")
    driver.get(url)
    
    # Ждём появления и исчезновения модального окна "Начало чата"
    if not wait_for_chat_modal(driver, timeout=300):
        print("❌ Чат не готов. Прерываем отправку.")
        return 'chat_not_ready'

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

        timeout = 30
        print("⌛ Ожидание готовности поля ввода...")
        input_box = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-placeholder="Введите сообщение"]'))
        )

        print("✅ Поле ввода найдено. Кликаем...")
        input_box.click()
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
        print(f"⚠️ Ошибка при отправке: {type(e).__name__}: {e}")
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

    profile_path = r'C:\Users\Merri\AppData\Roaming\Mozilla\Firefox\Profiles\z1hmvzj2.default'
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument('-profile')
    options.add_argument(profile_path)

    driver = webdriver.Firefox(options=options)

    driver.get('https://web.whatsapp.com/')

    print(Fore.CYAN + "🔎 Проверяю, залогинены ли вы в WhatsApp...")

    try:
        chat_list_xpath = '//div[@id="pane-side"]'
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, chat_list_xpath)))
        print(Fore.GREEN + "✅ Вы вошли в WhatsApp! Начинаем рассылку...")
    except Exception as e:
        print(Fore.RED + "❌ Не удалось войти в WhatsApp за 5 минут.")
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
            log_to_csv(SUCCESS_LOG.replace('.txt', '.csv'), [name, phone, message, timestamp ])
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
