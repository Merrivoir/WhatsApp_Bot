import os
import re

def check_phone_folders():
   
    directory = r"C:\MEGA\profiles\chrome"  # Директория для проверки
    phone_pattern = re.compile(r"^\d{10,12}$")  # Шаблон для телефонного номера от 10 до 12 цифр
    matching_folders = []

    # Перебор всех папок в указанной директории
    for item in os.listdir(directory):
        folder_path = os.path.join(directory, item)
        # Проверка, является ли элемент папкой и соответствует ли названию шаблону
        if os.path.isdir(folder_path) and phone_pattern.match(item):
            matching_folders.append(item)
    
    return matching_folders

# Пример использования:
matching_folders = check_phone_folders()

if matching_folders:
    print("Найдены следующие профили:")
    print("\n".join(matching_folders))
else:
    print("Профили отсутсвуют")