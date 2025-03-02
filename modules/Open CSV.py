import tkinter as tk
from tkinter import filedialog
import pandas as pd
import re

# Создаем корневое окно
root = tk.Tk()
# Скрываем корневое окно, чтобы показать только окно выбора файлов
root.withdraw()

# Открываем окно для выбора .csv файла
file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

# Если файл был выбран
if file_path:
    # Читаем .csv файл в DataFrame
    data = pd.read_csv(file_path)
    
    # Извлекаем имена и номера телефонов
    result = []
    numbers = []
    for _, row in data.iterrows():
        # Разделяем ФИО и берем только имя
        full_name = row.iloc[0]
        if isinstance(full_name, str):
            name = full_name.split()[0]  # Берем только первое слово как имя
        else:
            name = full_name  # Запасное значение, если имя отсутствует
        
        # Извлекаем номер телефона (предполагаем, что он в четвертом столбце)
        raw_number = str(row.iloc[3])
        
        # Очищаем номер телефона: удаляем все, кроме цифр
        number = re.sub(r'\D', '', raw_number)
        
        # Проверяем, что номер корректной длины (например, 11 символов для казахстанских номеров)
        if len(number) == 11:
            result.append([name, number])
            numbers.append(number)
        else:
            print(f"Неверный формат номера: {raw_number}")
    
    # Выводим результат
    print(numbers)
else:
    print('Файл не был выбран')
