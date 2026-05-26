from fastapi import APIRouter
from ..db import get_db
from ..models import Attendance
from ..face_service import recognize_face

router = APIRouter()


@router.post("/logout")
async def face_logout(file: bytes):
    """
    Same idea as login, but marks OUT
    (we will switch to webcam later)
    """

    # NOTE: simplified version (we will upgrade later with UploadFile)
    import numpy as np
    import cv2

    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    name = recognize_face(img)

    if name in ["no_face", "unknown"]:
        return {"success": False, "message": "Face not recognized"}

    db = next(get_db())

    record = Attendance(
        name=name,
        status="OUT"
    )

    db.add(record)
    db.commit()

    return {"success": True, "name": name, "status": "OUT"}