import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import *
import numpy as np
import threading

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Keyboard layout
keys = [
    ['ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'DEL'],
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Back'],
    ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Enter'],
    ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
    ['Space']
]

# Key size and spacing
key_w, key_h = 60, 60

# Tkinter fullscreen keyboard layout
root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black')
canvas.pack(fill=BOTH, expand=True)

key_boxes = []

def draw_keyboard():
    canvas.delete("all")
    key_boxes.clear()
    y = 100
    for row in keys:
        x = 100
        for key in row:
            w = key_w if key != 'Space' else 600
            box = canvas.create_rectangle(x, y, x + w, y + key_h, fill="gray", outline="white", width=2)
            text = canvas.create_text(x + w // 2, y + key_h // 2, text=key, fill="white", font=("Arial", 16, "bold"))
            key_boxes.append((key, x, y, x + w, y + key_h))
            x += w + 10
        y += key_h + 20

# Start webcam in another thread
cap = cv2.VideoCapture(0)

def is_pinch(hand_landmarks):
    tip = hand_landmarks.landmark[8]   # Index finger tip
    thumb_tip = hand_landmarks.landmark[4]  # Thumb tip

    dist = np.sqrt((tip.x - thumb_tip.x) ** 2 + (tip.y - thumb_tip.y) ** 2)
    return dist < 0.03  # Adjust sensitivity if needed

def click_key(finger_x, finger_y):
    for key, x1, y1, x2, y2 in key_boxes:
        if x1 <= finger_x <= x2 and y1 <= finger_y <= y2:
            canvas.itemconfig("all", fill="gray")  # reset all keys
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="white", width=2)
            canvas.create_text((x1+x2)//2, (y1+y2)//2, text=key, fill="white", font=("Arial", 16, "bold"))
            pyautogui.press(key.lower() if len(key) == 1 else key.lower())
            break

def webcam_loop():
    last_pressed = ''
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)

        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[0]
            h, w, c = img.shape
            cx = int(handLms.landmark[8].x * root.winfo_screenwidth())
            cy = int(handLms.landmark[8].y * root.winfo_screenheight())
            
            if is_pinch(handLms):
                if last_pressed != (cx, cy):
                    click_key(cx, cy)
                    last_pressed = (cx, cy)
            else:
                last_pressed = ''
        cv2.waitKey(1)

# Launch keyboard and webcam
draw_keyboard()
threading.Thread(target=webcam_loop, daemon=True).start()
root.mainloop()
cap.release()
