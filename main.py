import os
import datetime

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util
from models.face_db import init_db, add_user, log_attendance


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Face Attendance System")

        # Initialize database
        init_db()

        # ---------------- BUTTONS ----------------
        self.login_button = util.get_button(
            self.main_window, 'LOGIN', 'green', self.login
        )
        self.login_button.place(x=750, y=200)

        self.logout_button = util.get_button(
            self.main_window, 'LOGOUT', 'red', self.logout
        )
        self.logout_button.place(x=750, y=300)

        self.register_button = util.get_button(
            self.main_window, 'REGISTER', 'gray',
            self.register_new_user, fg='black'
        )
        self.register_button.place(x=750, y=400)

        # ---------------- CAMERA ----------------
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.cap = cv2.VideoCapture(0)
        self.process_webcam()

    # ---------------- WEBCAM LOOP ----------------
    def process_webcam(self):
        ret, frame = self.cap.read()

        if not ret:
            self.main_window.after(20, self.process_webcam)
            return

        self.most_recent_capture_arr = frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(rgb)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)

        self.webcam_label.after(20, self.process_webcam)

    # ---------------- LOGIN ----------------
    def login(self):
        name = util.recognize(self.most_recent_capture_arr)

        if name in ["unknown_person", "no_persons_found"]:
            util.msg_box("Error", "Unknown user")
        else:
            util.msg_box("Welcome", f"Welcome {name}")
            log_attendance(name, "IN")

    # ---------------- LOGOUT ----------------
    def logout(self):
        name = util.recognize(self.most_recent_capture_arr)

        if name in ["unknown_person", "no_persons_found"]:
            util.msg_box("Error", "Unknown user")
        else:
            util.msg_box("Yalla", f"Goodbye {name}")
            log_attendance(name, "OUT")

    # ---------------- REGISTER ----------------
    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x520+370+120")
        self.register_window.title("Register New User")

        # Capture preview
        self.capture_label = util.get_img_label(self.register_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        rgb = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.register_capture = self.most_recent_capture_arr.copy()

        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.capture_label.imgtk = imgtk
        self.capture_label.configure(image=imgtk)

        # Input
        self.entry_text = util.get_entry_text(self.register_window)
        self.entry_text.place(x=750, y=150)

        self.label = util.get_text_label(self.register_window, "Enter Username:")
        self.label.place(x=750, y=70)

        # Buttons
        self.accept_button = util.get_button(
            self.register_window,
            "SAVE",
            "green",
            self.save_user
        )
        self.accept_button.place(x=750, y=300)

        self.cancel_button = util.get_button(
            self.register_window,
            "CANCEL",
            "red",
            self.register_window.destroy
        )
        self.cancel_button.place(x=750, y=400)

    # ---------------- SAVE USER ----------------
    def save_user(self):
        name = self.entry_text.get(1.0, "end-1c").strip()

        if name == "":
            util.msg_box("Error", "Name cannot be empty")
            return

        encodings = face_recognition.face_encodings(self.register_capture)

        if len(encodings) == 0:
            util.msg_box("Error", "No face detected")
            return

        add_user(name, encodings[0])

        util.msg_box("Success", f"User {name} registered")
        self.register_window.destroy()

    # ---------------- START APP ----------------
    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()