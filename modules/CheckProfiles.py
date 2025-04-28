import os
import re

def check_phone_folders():
   
    directory_chrome = r"C:\Msync\profiles\chrome"  # Директория для проверки
    directory_firefox = r"C:\Msync\profiles\firefox"
    phone_pattern = re.compile(r"^\d{10,12}$")  # Шаблон для телефонного номера от 10 до 12 цифр
    matching_chrome = []
    matching_firefox = []

    # Перебор всех папок в указанной директории
    for item in os.listdir(directory_chrome):
        folder_path = os.path.join(directory_chrome, item)
        # Проверка, является ли элемент папкой и соответствует ли названию шаблону
        if os.path.isdir(folder_path) and phone_pattern.match(item):
            matching_chrome.append(item)

    for item in os.listdir(directory_firefox):
        folder_path = os.path.join(directory_firefox, item)
        # Проверка, является ли элемент папкой и соответствует ли названию шаблону
        if os.path.isdir(folder_path) and phone_pattern.match(item):
            matching_firefox.append(item)
    
    return [matching_chrome, matching_firefox]

# Пример использования:
matching_folders = check_phone_folders()

if matching_folders:
    print("Найдены следующие профили Chrome:")
    print("\n".join(matching_folders[0]))
    print("Найдены следующие профили Firefox:")
    print("\n".join(matching_folders[1]))
else:
    print("Профили отсутсвуют")