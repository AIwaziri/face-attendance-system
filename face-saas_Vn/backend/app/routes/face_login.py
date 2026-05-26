from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2

from ..db import get_db
from ..models import Attendance
from ..face_service import recognize_face

router = APIRouter()


@router.post("/login")
async def face_login(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    name = recognize_face(img)

    if name == "no_face":
        return {
            "success": False,
            "message": "No face detected"
        }

    if name == "unknown":
        return {
            "success": False,
            "message": "Unknown user"
        }

    db = next(get_db())

    attendance = Attendance(
        name=name,
        status="IN"
    )

    db.add(attendance)
    db.commit()

    return {
        "success": True,
        "name": name,
        "status": "IN"
    }
