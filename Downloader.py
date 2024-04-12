import youtube_dl
import pyperclip
import tkinter as tk
from tkinter import messagebox
import threading
import time

auto_download_enabled = False
auto_download_button = None  # Змінна для збереження кнопки
last_link = None  # Змінна для збереження останнього посилання
downloading = False  # Змінна, що вказує, чи в даний момент виконується завантаження

def download_video(url):
    global downloading
    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if auto_download_enabled:
            pyperclip.copy("")  # Очищення буфера обміну після автоматичного завантаження
        downloading = False
    except Exception as e:
        print(f"Помилка при завантаженні відео: {e}")
        downloading = False

def handle_download():
    global last_link
    global downloading
    # Отримати текс з буфера обміну
    clipboard_content = pyperclip.paste().strip()
    if clipboard_content and clipboard_content != last_link and not downloading:
        if clipboard_content.startswith("https://") or clipboard_content.startswith("http://"):
            last_link = clipboard_content
            downloading = True
            download_thread = threading.Thread(target=download_video, args=(clipboard_content,))
            download_thread.start()
        else:
            print("Це не валідне посилання.")
    else:
        print("Буфер обміну порожній або вже завантажено.")

def toggle_auto_download():
    global auto_download_enabled
    auto_download_enabled = not auto_download_enabled
    if auto_download_enabled:
        auto_download_button.config(text="Авто-завантаження: Включено")
        auto_download_check()
    else:
        auto_download_button.config(text="Авто-завантаження: Вимкнено")

def auto_download_check():
    if auto_download_enabled:
        handle_download()
        # Виконувати перевірку кожні 5 секунд
        threading.Timer(0.1, auto_download_check).start()

def clear_clipboard():
    pyperclip.copy("")
    print("Буфер обміну успішно очищено.")

def main():
    global auto_download_button  # Оголошення кнопки як глобальної
    root = tk.Tk()
    root.title("Завантаження відео")
    root.geometry("300x150")

    label = tk.Label(root, text="Натисніть кнопку, щоб завантажити відео з URL-адреси в буфері обміну:")
    label.pack(pady=5)

    auto_download_button = tk.Button(root, text="Авто-завантаження: Вимкнено", command=toggle_auto_download)
    auto_download_button.pack(pady=5)

    clear_button = tk.Button(root, text="Очистити буфер обміну", command=clear_clipboard)
    clear_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
