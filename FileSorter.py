import os
import shutil
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

TRANSLATIONS = {
    "en": {
        "title": "File Sorter",
        "instruction": "Please select the folder where files need to be sorted,\nor enter the path manually.",
        "browse": "Browse",
        "start": "Start sorting",
        "settings": "Settings",
        "settings_title": "Settings",
        "settings_instruction": "Choose the sorting method:",
        "sort_by_extensions": "Sort by extension",
        "sort_by_creation_date": "Sort by creation date",
        "close": "Close",
        "toggle": "RU",
        "completed_title": "Completed",
        "completed_message": "Sorting completed!",
        "error_title": "Error",
        "folder_required": "Please specify a folder to sort!",
        "folder_missing": "The folder does not exist!",
        "moved_file": "Moved file: {filename} -> {folder_name}",
        "results_header": "\nSorting results:",
        "sorted_count": "\nSorted {folder_name}: {count}",
        "total_count": "\nTotal files: {count}",
        "end": "Sorting finished",
    },
    "ru": {
        "title": "Сортировщик файлов",
        "instruction": "Пожалуйста, выберите папку, в которой необходимо\nотсортировать файлы, либо введите путь вручную.",
        "browse": "Обзор",
        "start": "Начать сортировку",
        "settings": "Настройки",
        "settings_title": "Настройки",
        "settings_instruction": "Выберите способ сортировки:",
        "sort_by_extensions": "Сортировать по расширениям",
        "sort_by_creation_date": "Сортировать по дате создания",
        "close": "Закрыть",
        "toggle": "EN",
        "completed_title": "Выполнено",
        "completed_message": "Сортировка завершена!",
        "error_title": "Ошибка",
        "folder_required": "Укажите папку для сортировки!",
        "folder_missing": "Папка не существует!",
        "moved_file": "Перемещён файл: {filename} -> {folder_name}",
        "results_header": "\nРезультаты сортировки:",
        "sorted_count": "\nОтсортировано {folder_name}: {count}",
        "total_count": "\nОбщее количество: {count}",
        "end": "Конец сортировки",
    },
}


def sort_img(sf, lang, sort_mode):
    texts = TRANSLATIONS[lang]
    extension_counts = {}
    moved_count = 0

    for filename in os.listdir(sf):
        file_path = os.path.join(sf, filename)

        if not os.path.isfile(file_path):
            continue

        if sort_mode == "date":
            creation_time = os.path.getctime(file_path)
            folder_name = time.strftime("%Y-%m-%d", time.localtime(creation_time))
        else:
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
        print(texts["moved_file"].format(filename=filename, folder_name=folder_name))

    print(texts["results_header"])
    for folder_name, count in sorted(extension_counts.items()):
        print(texts["sorted_count"].format(folder_name=folder_name, count=count))
    print(texts["total_count"].format(count=moved_count))
    print(texts["end"])

    messagebox.showinfo(texts["completed_title"], texts["completed_message"])


mw = tk.Tk()
current_lang = "en"
sort_mode = tk.StringVar(value="extension")
settings_window = None
settings_widgets = {}

mw.title(TRANSLATIONS[current_lang]["title"])
mw.geometry('410x140')
mw.resizable(False, False)

header_frame = tk.Frame(mw)
header_frame.pack(fill=tk.X, padx=10, pady=(10, 6))

label_var = tk.StringVar(value=TRANSLATIONS[current_lang]["instruction"])
label = tk.Label(header_frame, textvariable=label_var, justify="center", wraplength=430)
label.pack(side=tk.LEFT, expand=True)


def toggle_language():
    global current_lang
    current_lang = "ru" if current_lang == "en" else "en"
    texts = TRANSLATIONS[current_lang]
    mw.title(texts["title"])
    label_var.set(texts["instruction"])
    browse_button.config(text=texts["browse"])
    start_button.config(text=texts["start"])
    lang_button.config(text=texts["toggle"])
    settings_button.config(text=texts["settings"])

    if settings_window is not None and settings_window.winfo_exists():
        update_settings_texts()


fp = tk.Frame(mw)
fp.pack(pady=6)

ep = tk.Entry(fp, width=32)
ep.pack(side=tk.LEFT, padx=6)


def bf():
    sf = filedialog.askdirectory()
    if sf:
        ep.delete(0, tk.END)
        ep.insert(0, sf)


def update_settings_texts():
    texts = TRANSLATIONS[current_lang]
    settings_window.title(texts["settings_title"])
    settings_widgets["instruction_label"].config(text=texts["settings_instruction"])
    settings_widgets["rb_extension"].config(text=texts["sort_by_extensions"])
    settings_widgets["rb_date"].config(text=texts["sort_by_creation_date"])
    settings_widgets["close_button"].config(text=texts["close"])


def close_settings():
    global settings_window, settings_widgets
    if settings_window is not None and settings_window.winfo_exists():
        settings_window.destroy()
    settings_window = None
    settings_widgets = {}


def open_settings():
    global settings_window, settings_widgets
    texts = TRANSLATIONS[current_lang]
    if settings_window is not None and settings_window.winfo_exists():
        settings_window.lift()
        return

    settings_window = tk.Toplevel(mw)
    settings_window.title(texts["settings_title"])
    settings_window.resizable(False, False)
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)

    instruction_label = tk.Label(settings_window, text=texts["settings_instruction"], justify="left")
    instruction_label.pack(padx=12, pady=(12, 6), anchor="w")

    rb_extension = tk.Radiobutton(settings_window, text=texts["sort_by_extensions"], variable=sort_mode, value="extension")
    rb_extension.pack(anchor="w", padx=14, pady=2)
    rb_date = tk.Radiobutton(settings_window, text=texts["sort_by_creation_date"], variable=sort_mode, value="date")
    rb_date.pack(anchor="w", padx=14, pady=(0, 10))

    close_button = ttk.Button(settings_window, text=texts["close"], command=close_settings)
    close_button.pack(pady=(0, 10))

    settings_widgets = {
        "instruction_label": instruction_label,
        "rb_extension": rb_extension,
        "rb_date": rb_date,
        "close_button": close_button,
    }


def ss():
    sf = ep.get()
    if not sf:
        messagebox.showerror(TRANSLATIONS[current_lang]["error_title"], TRANSLATIONS[current_lang]["folder_required"])
        return
    if not os.path.exists(sf):
        messagebox.showerror(TRANSLATIONS[current_lang]["error_title"], TRANSLATIONS[current_lang]["folder_missing"])
        return

    sort_img(sf, current_lang, sort_mode.get())


browse_button = ttk.Button(fp, text=TRANSLATIONS[current_lang]["browse"], command=bf)
browse_button.pack(side=tk.LEFT)

button_frame = tk.Frame(mw)
button_frame.pack(pady=6)

lang_button = ttk.Button(button_frame, text=TRANSLATIONS[current_lang]["toggle"], width=4, command=toggle_language)
lang_button.pack(side=tk.LEFT, padx=4)
settings_button = ttk.Button(button_frame, text=TRANSLATIONS[current_lang]["settings"], command=open_settings)
settings_button.pack(side=tk.LEFT, padx=4)
start_button = ttk.Button(button_frame, text=TRANSLATIONS[current_lang]["start"], command=ss)
start_button.pack(side=tk.LEFT, padx=4)


def on_closing():
    mw.destroy()


mw.protocol("WM_DELETE_WINDOW", on_closing)
mw.mainloop()