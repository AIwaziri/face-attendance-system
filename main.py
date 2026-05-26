import os
import datetime
import pickle

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition

import util


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.title("Face Attendance System")

        # Buttons
        self.login_button_main_window = util.get_button(
            self.main_window, 'login', 'green', self.login
        )
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(
            self.main_window, 'logout', 'red', self.logout
        )
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(
            self.main_window, 'register new user', 'gray',
            self.register_new_user, fg='black'
        )
        self.register_new_user_button_main_window.place(x=750, y=400)

        # Webcam
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        # DB
        self.db_dir = './db'
        os.makedirs(self.db_dir, exist_ok=True)

        self.log_path = './log.txt'

    # ---------------- WEBCAM ----------------
    def add_webcam(self, label):
        if not hasattr(self, 'cap'):
            self.cap = cv2.VideoCapture(0)  # 0 = default Mac camera

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if not ret:
            self._label.after(20, self.process_webcam)
            return

        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    # ---------------- LOGIN ----------------
    def login(self):
        name = self.recognize_face()

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register first.')
        else:
            util.msg_box('Welcome', f'Welcome back, {name}')
            self.log_event(name, "in")

    # ---------------- LOGOUT ----------------
    def logout(self):
        name = self.recognize_face()

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oops...', 'Unknown user. Please register first.')
        else:
            util.msg_box('Goodbye', f'Goodbye, {name}')
            self.log_event(name, "out")

    # ---------------- FACE RECOGNITION ----------------
    def recognize_face(self):
        try:
            face_locations = face_recognition.face_locations(self.most_recent_capture_arr)
            encodings = face_recognition.face_encodings(self.most_recent_capture_arr, face_locations)

            if len(encodings) == 0:
                return "no_persons_found"

            encoding = encodings[0]

            for file in os.listdir(self.db_dir):
                if not file.endswith('.pickle'):
                    continue

                path = os.path.join(self.db_dir, file)
                with open(path, 'rb') as f:
                    stored_encoding = pickle.load(f)

                match = face_recognition.compare_faces([stored_encoding], encoding)[0]

                if match:
                    return file.replace('.pickle', '')

            return "unknown_person"

        except Exception as e:
            print("Recognition error:", e)
            return "error"

    # ---------------- REGISTER ----------------
    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x520+370+120")

        self.capture_label = util.get_img_label(self.register_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self.capture_label.imgtk = imgtk
        self.capture_label.configure(image=imgtk)

        self.register_capture = self.most_recent_capture_arr.copy()

        self.entry_text = util.get_entry_text(self.register_window)
        self.entry_text.place(x=750, y=150)

        self.text_label = util.get_text_label(self.register_window, "Enter username:")
        self.text_label.place(x=750, y=70)

        self.accept_button = util.get_button(
            self.register_window, 'accept', 'green', self.save_new_user
        )
        self.accept_button.place(x=750, y=300)

        self.cancel_button = util.get_button(
            self.register_window, 'cancel', 'red', self.register_window.destroy
        )
        self.cancel_button.place(x=750, y=400)

    def save_new_user(self):
        name = self.entry_text.get(1.0, "end-1c")

        encodings = face_recognition.face_encodings(self.register_capture)

        if len(encodings) == 0:
            util.msg_box("Error", "No face detected!")
            return

        encoding = encodings[0]

        file_path = os.path.join(self.db_dir, f"{name}.pickle")

        with open(file_path, 'wb') as f:
            pickle.dump(encoding, f)

        util.msg_box("Success", f"User {name} registered!")
        self.register_window.destroy()

    # ---------------- LOGGING ----------------
    def log_event(self, name, event_type):
        with open(self.log_path, 'a') as f:
            f.write(f"{name},{datetime.datetime.now()},{event_type}\n")

    # ---------------- START ----------------
    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()