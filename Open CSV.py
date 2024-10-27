import tkinter as tk
from tkinter import filedialog
import pandas as pd

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
    
    # Выводим данные
    print(data)
else:
    print('Файл не был выбран')