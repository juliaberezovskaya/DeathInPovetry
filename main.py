import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import winsound

# ===== НАСТРОЙКИ =====
GAME_ID = 570                           # Dota 2
BUTTON_RADIUS = 80                      # радиус зоны клика
ACCEPT_CENTER = (80, 330)              # координаты зелёной трубки
DECLINE_CENTER = (185, 330)              # координаты красной трубки
BG_COLOR = "black"
IMG_FILE = "call.png"
SOUND_FILE = "ring.wav"
# =====================

def resource_path(filename: str) -> str:
    """Возвращает путь к ресурсу как при запуске .py, так и в собранном exe"""
    if getattr(sys, 'frozen', False):  # Если запущено из exe
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

IMG_PATH = resource_path(IMG_FILE)
SOUND_PATH = resource_path(SOUND_FILE)

def stop_sound():
    winsound.PlaySound(None, winsound.SND_PURGE)

def play_sound_loop():
    winsound.PlaySound(SOUND_PATH, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

def launch_game():
    stop_sound()
    webbrowser.open(f"steam://rungameid/{GAME_ID}")
    root.destroy()

def decline():
    stop_sound()
    root.destroy()

root = tk.Tk()
root.configure(bg=BG_COLOR)
root.overrideredirect(True)  # без рамки и заголовка

# Загружаем картинку
img = Image.open(IMG_PATH)
photo = ImageTk.PhotoImage(img)
img_w, img_h = img.size

canvas = tk.Canvas(root, width=img_w, height=img_h, highlightthickness=0, bd=0, bg=BG_COLOR)
canvas.pack()
canvas.create_image(0, 0, image=photo, anchor="nw")

# Проверка попадания в круг
def inside_circle(px, py, cx, cy, r):
    return (px - cx)**2 + (py - cy)**2 <= r**2

# Обработка кликов
def on_click(event):
    if inside_circle(event.x, event.y, *ACCEPT_CENTER, BUTTON_RADIUS):
        launch_game()
    elif inside_circle(event.x, event.y, *DECLINE_CENTER, BUTTON_RADIUS):
        decline()

def on_motion(event):
    inside = (
        inside_circle(event.x, event.y, *ACCEPT_CENTER, BUTTON_RADIUS) or
        inside_circle(event.x, event.y, *DECLINE_CENTER, BUTTON_RADIUS)
    )
    canvas.config(cursor="hand2" if inside else "")

canvas.bind("<Button-1>", on_click)
canvas.bind("<Motion>", on_motion)

# Центровка окна
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - img_w) // 2
y = (screen_h - img_h) // 2
root.geometry(f"{img_w}x{img_h}+{x}+{y}")

# Запуск звука
play_sound_loop()

root.mainloop()
