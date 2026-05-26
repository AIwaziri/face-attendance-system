import tkinter as tk
from tkinter import messagebox
import face_recognition
from models.face_db import get_all_users


# ---------------- UI HELPERS ----------------

def get_button(window, text, color, command, fg='white'):
    return tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica', 16, 'bold')
    )


def get_img_label(window):
    label = tk.Label(window)
    label.place(x=0, y=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Arial", 18))
    return label


def get_entry_text(window):
    return tk.Text(
        window,
        height=2,
        width=15,
        font=("Arial", 24)
    )


def msg_box(title, description):
    messagebox.showinfo(title, description)


# ---------------- FACE RECOGNITION ----------------

def recognize(img):
    unknown_faces = face_recognition.face_encodings(img)

    if len(unknown_faces) == 0:
        return "no_persons_found"

    unknown = unknown_faces[0]

    users = get_all_users()

    best_match = None
    best_distance = 0.5  # stricter threshold for real system

    for name, embedding in users:
        distance = face_recognition.face_distance([embedding], unknown)[0]

        if distance < best_distance:
            best_distance = distance
            best_match = name

    return best_match if best_match else "unknown_person"