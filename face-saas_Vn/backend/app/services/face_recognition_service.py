import face_recognition
import numpy as np
import pickle

from app.db import SessionLocal
from app.models import User


def encode_face(image):
    enc = face_recognition.face_encodings(image)
    return enc[0] if len(enc) > 0 else None


def recognize_face(image):
    unknown = encode_face(image)

    if unknown is None:
        return "no_face"

    db = SessionLocal()
    users = db.query(User).all()

    best_match = None
    best_distance = 0.5

    for user in users:
        if user.embedding is None:
            continue

        stored = pickle.loads(user.embedding)

        dist = face_recognition.face_distance([stored], unknown)[0]

        if dist < best_distance:
            best_distance = dist
            best_match = user.name

    return best_match or "unknown"