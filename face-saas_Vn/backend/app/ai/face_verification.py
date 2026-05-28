from app.ai.face_model import extract_embedding
from app.ai.liveness import is_blinking
import numpy as np
import pickle


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    return float(np.dot(a, b))


def verify_face(frame, stored_embedding):

    # 1. Liveness check
    if not is_blinking(frame):
        return {"status": "rejected", "reason": "no liveness detected"}

    # 2. Extract embedding
    embedding = extract_embedding(frame)

    if embedding is None or len(embedding) == 0:
        return {"status": "rejected", "reason": "invalid face embedding"}

    # 3. Decode stored embedding
    if stored_embedding is None:
        return {"status": "rejected", "reason": "no stored embedding"}

    if isinstance(stored_embedding, (bytes, bytearray)):
        stored_embedding = pickle.loads(stored_embedding)

    embedding = np.asarray(embedding, dtype=np.float32)
    stored_embedding = np.asarray(stored_embedding, dtype=np.float32)

    # 4. Similarity
    score = cosine_similarity(embedding, stored_embedding)

    THRESHOLD = 0.5

    if score > THRESHOLD:
        return {"status": "accepted", "score": score}

    return {"status": "rejected", "reason": "face mismatch", "score": score}