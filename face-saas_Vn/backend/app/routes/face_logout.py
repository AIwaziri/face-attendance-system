from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2

from ..db import get_db
from ..models import Attendance
from ..face_service import recognize_face

router = APIRouter()

@router.post("/logout")
async def logout(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    name = recognize_face(img)

    if name in ["no_face", "unknown"]:
        return {"success": False, "message": "Face not recognized"}

    db = next(get_db())

    db.add(Attendance(
        name=name,
        status="OUT"
    ))

    db.commit()

    return {"success": True, "name": name, "status": "OUT"}