from fastapi import APIRouter, UploadFile, File, Form
import numpy as np
import cv2
import pickle

from ..db import get_db, engine
from ..models import User, Base
from ..face_service import encode_face

router = APIRouter()

# create tables safely (IMPORTANT FIX)
Base.metadata.create_all(bind=engine)


@router.post("/register")
async def register_user(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    encoding = encode_face(img)

    if encoding is None:
        return {"error": "No face detected"}

    db = next(get_db())

    user = User(
        name=name,
        embedding=pickle.dumps(encoding)
    )

    db.add(user)
    db.commit()

    return {"message": f"{name} registered successfully"}

