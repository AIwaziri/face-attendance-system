import os
import pickle
import tkinter as tk
from tkinter import messagebox
import face_recognition


# ---------------- UI COMPONENTS ----------------

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
    label.place(x=0, y=0)   # FIXED: consistent with .place() in main.py
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Arial", 18), justify="left")
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

def recognize(img, db_path):
    """
    Compare webcam face with stored embeddings in db_path.
    Returns: username / unknown_person / no_persons_found
    """

    # Step 1: extract face encoding from input image
    embeddings_unknown = face_recognition.face_encodings(img)

    if len(embeddings_unknown) == 0:
        return 'no_persons_found'

    embeddings_unknown = embeddings_unknown[0]

    # Step 2: load DB files
    if not os.path.exists(db_path):
        return 'unknown_person'

    db_files = [f for f in os.listdir(db_path) if f.endswith('.pickle')]
    db_files.sort()

    # Step 3: compare with stored embeddings
    for file in db_files:
        file_path = os.path.join(db_path, file)

        try:
            with open(file_path, 'rb') as f:
                stored_embedding = pickle.load(f)
        except Exception as e:
            print(f"Error loading {file}: {e}")
            continue

        # Better accuracy than compare_faces
        distance = face_recognition.face_distance(
            [stored_embedding],
            embeddings_unknown
        )[0]

        # threshold (lower = stricter)
        if distance < 0.5:
            return os.path.splitext(file)[0]

    return 'unknown_person'