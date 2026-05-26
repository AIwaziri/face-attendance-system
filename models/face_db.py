import sqlite3
import numpy as np
import pickle
import os
from datetime import datetime


DB_PATH = "db.sqlite3"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            embedding BLOB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            timestamp TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(name, embedding):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = pickle.dumps(embedding)

    cursor.execute(
        "INSERT OR REPLACE INTO users (name, embedding) VALUES (?, ?)",
        (name, data)
    )

    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, embedding FROM users")
    rows = cursor.fetchall()

    conn.close()

    users = []
    for name, emb in rows:
        users.append((name, pickle.loads(emb)))

    return users


def log_attendance(name, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance (name, timestamp, status)
        VALUES (?, ?, ?)
    """, (name, str(datetime.now()), status))

    conn.commit()
    conn.close()