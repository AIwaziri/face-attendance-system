
# Face Recognition Attendance System
A real-time AI-powered attendance system that uses facial recognition to register users and automatically log attendance (IN / OUT). Built with Python, OpenCV, and SQLite, this project demonstrates a full computer vision pipeline from face detection to identity matching and database logging.
---
# 🚀 Overview
This system captures live webcam video, detects faces in real time, compares them against stored user embeddings, and logs attendance automatically.
It replaces manual attendance systems with a fast, contactless, AI-driven solution.
---
# ⚡ Key Features
- 🎥 Real-time webcam face detection
- 🧑 Face recognition using deep learning embeddings
- 📝 User registration with live face capture
- 🗄️ SQLite database storage (no pickle files or CSV dependency)
- 📊 Attendance logging (IN / OUT with timestamps)
- 🖥️ Simple and interactive Tkinter GUI
- ⚡ Offline system (no internet required)
- 🔐 Scalable and modular architecture
---
# 🧠 How It Works
## 1. Face Registration
- User enters a name
- System captures face from webcam
- Face encoding is generated using `face_recognition`
- Encoding is stored in SQLite database
## 2. Face Recognition
- Webcam continuously captures frames
- Each frame is converted into face embeddings
- Embeddings are compared with stored users
- Best match is returned based on distance threshold
## 3. Attendance Logging
- If user is recognized:
  - LOGIN → logs "IN"
  - LOGOUT → logs "OUT"
- Stored in SQLite database with timestamp
---
# 🏗️ System Architecture

Frontend (Tkinter UI)
↓
Webcam Capture (OpenCV)
↓
Face Encoding (face_recognition / dlib)
↓
Matching Engine (Euclidean Distance)
↓
SQLite Database (Users + Attendance)

---
# 📂 Project Structure

face-attendance-system/
│
├── main.py              # Main application (UI + workflow)
├── util.py              # Face recognition + UI helper functions
├── models/
│   └── face_db.py      # Database layer (SQLite operations)
│
├── db.sqlite3          # Auto-generated database file
└── README.md

---
# 🗄️ Database Schema
## Users Table
| Field     | Type    | Description              |
|----------|--------|--------------------------|
| id       | INT     | Primary key              |
| name     | TEXT    | Username                 |
| embedding| BLOB    | Face encoding vector     |
## Attendance Table
| Field     | Type    | Description              |
|----------|--------|--------------------------|
| id       | INT     | Primary key              |
| name     | TEXT    | Username                 |
| timestamp| TEXT    | Date and time of event   |
| status   | TEXT    | IN / OUT                 |
---
## ⚙️ Installation

1. Clone the repository


git clone https://github.com/AIwaziri/face-attendance-system.git
2. Create virtual environment

Mac / Linux

python -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

⸻

3. Install dependencies

pip install opencv-python face_recognition pillow numpy

⸻

▶️ Run the Application

python main.py

⸻

🧑‍💻 Usage Guide

Step 1: Register User

* Click “Register”
* Enter username
* Capture face
* Save user

Step 2: Login Attendance

* Look at camera
* Click “LOGIN”
* System detects face and logs attendance

Step 3: Logout Attendance

* Click “LOGOUT”
* System logs exit time

⸻

🧠 Technologies Used

* Python 3.x
* OpenCV (computer vision)
* face_recognition (dlib-based embeddings)
* Tkinter (GUI)
* SQLite (database)
* Pillow (image processing)

⸻

🔐 Security Considerations

* Local-only biometric storage
* No external API calls
* Future improvements:
    * Face liveness detection (anti-spoofing)
    * Encrypted embeddings
    * Secure authentication layer

⸻

📊 Performance

* Real-time processing (~20 FPS depending on system)
* Lightweight local execution
* Fast recognition using embedding distance comparison

⸻

🚀 Future Improvements

* 🌐 Web dashboard (FastAPI / React)
* ☁️ Cloud database integration (AWS / Azure)
* 👥 Multi-face tracking per frame
* 🛡️ Anti-spoofing (blink / depth detection)
* 📱 Mobile app integration
* 📈 Analytics dashboard for HR systems
* ⚡ FAISS vector search for large-scale deployments

⸻

📸 Screenshots (Optional)

Add screenshots of:

* Login screen
* Webcam detection
* Registration window
* Attendance logs

⸻

👨‍💻 Author

Built by Ai Waziri

AI Engineer | Software Developer | System Architect
