#code by Ilya Memory 2025
import os 
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def sort_img(sf):
    extension_counts = {}
    moved_count = 0

    for filename in os.listdir(sf):
        file_path = os.path.join(sf, filename)

        if not os.path.isfile(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower().lstrip('.')
        folder_name = extension if extension else 'no_extension'
        target_folder = os.path.join(sf, folder_name)

        os.makedirs(target_folder, exist_ok=True)

        destination_path = os.path.join(target_folder, filename)
        if os.path.exists(destination_path):
            base_name, file_extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(target_folder, f'{base_name} ({counter}){file_extension}')):
                counter += 1
            destination_path = os.path.join(target_folder, f'{base_name} ({counter}){file_extension}')

        shutil.move(file_path, destination_path)
        moved_count += 1
        extension_counts[folder_name] = extension_counts.get(folder_name, 0) + 1
        print(f'Перемещён файл: {filename} -> {folder_name}')

    print('\n Результаты сортировки:')
    for folder_name, count in sorted(extension_counts.items()):
        print(f'\n Отсортированно {folder_name}: {count}')
    print(f'\n Общее количество: {moved_count}')
    print('Конец сортировки')

    messagebox.showinfo("Выполнено", "Сортировка завершена!")

mw = tk.Tk()
mw.title('Сортировщик JPEG и PNG')
mw.geometry('500x200')
mw.resizable(False, False)

label = tk.Label(mw, text='Пожалуйста, выберите папку в которой необходимо \n отсортировать файлы, либо введите вручную')
label.pack(pady=20)

fp = tk.Frame(mw) #frame_path - рамка для поля ввода и кнопки обзор
fp.pack(pady=7)

ep = tk.Entry(fp, width=30) #entry_path - поле ввода
ep.pack(side=tk.LEFT, padx=10)

def bf(): #browse_folder - функция вызывающая окно выбора папки
    sf = filedialog.askdirectory()
    if sf:
        ep.delete(0, tk.END)
        ep.insert(0, sf)

def ss(): #start_sorting
    sf = ep.get()
    if not sf:
        messagebox.showerror("Ошибка", "Укажите папку для сортировки!")
        return
    if not os.path.exists(sf):
        messagebox.showerror("Ошибка", "Папка не существует!")
        return
    
    sort_img(sf)

tk.Button(fp, text='Обзор', command=bf).pack(side=tk.LEFT)
tk.Button(mw, text='Начать сортировку', command=ss).pack(pady=30)

mw.mainloop()