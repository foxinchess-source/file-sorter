#code by Ilya Memory 2025
import os 
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def sort_img(sf):
    jpeg_folder = os.path.join(sf, 'Jpeg')
    png_folder = os.path.join(sf, 'Png')

    os.makedirs(jpeg_folder, exist_ok=True)
    os.makedirs(png_folder, exist_ok=True)

    jpeg_count = 0
    png_count = 0

    for filename in os.listdir(sf):
        file_path = os.path.join(sf, filename)

        if not os.path.isfile(file_path):
            continue

        if filename.lower().endswith(('.jpeg', '.jpg')):
            shutil.move(file_path, os.path.join(jpeg_folder, filename))
            jpeg_count += 1
            print(f'Перемещён JPEG: {filename}')

        elif filename.lower().endswith('.png'):
            shutil.move(file_path, os.path.join(png_folder, filename))
            png_count += 1
            print(f'Перемещён PNG: {filename}')

    print('\n Результаты сортировки:')
    print(f'\n Отсортированно JPEG: {jpeg_count}')
    print(f'\n Отсортированно PNG: {png_count}')
    print(f'\n Общее количество: {png_count + jpeg_count}')
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