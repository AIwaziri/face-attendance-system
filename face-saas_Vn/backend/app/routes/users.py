from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import numpy as np
import cv2
import pickle

from ..db import get_db
from ..models import User
from ..services.face_recognition_service import encode_face

router = APIRouter()


@router.post("/register")
async def register_user(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(400, "Invalid image")

    encoding = encode_face(img)

    if encoding is None:
        raise HTTPException(400, "No face detected")

    existing = db.query(User).filter(User.name == name).first()
    if existing:
        raise HTTPException(400, "User already exists")

    user = User(
        name=name,
        embedding=pickle.dumps(encoding)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "user_id": user.id
    }


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {"id": u.id, "name": u.name}
        for u in users
    ]