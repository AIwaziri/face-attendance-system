from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import cv2
import numpy as np
import pickle

from ..db import get_db
from ..auth_deps import get_current_user
from ..ai.face_verification import verify_face

router = APIRouter()


@router.post("/verify")
def face_login(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    image_bytes = np.frombuffer(file.file.read(), np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    if user.embedding is None:
        return {"error": "No embedding found for user"}

    result = verify_face(frame, user.embedding)

    return {
        "user": user.name,
        "result": result
    }