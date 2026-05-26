from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from datetime import datetime, timedelta

from ..db import get_db
from ..models import User, Attendance
from ..face_service import recognize_face
from ..websocket import manager
from ..anti_spoof_ai import is_real_face
router = APIRouter()

last_seen = {}
COOLDOWN_SECONDS = 10


def can_process(name: str):
    now = datetime.utcnow()

    if name in last_seen:
        if now - last_seen[name] < timedelta(seconds=COOLDOWN_SECONDS):
            return False

    last_seen[name] = now
    return True


@router.post("/scan")
async def face_scan(file: UploadFile = File(...)):
    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    name = recognize_face(img)

    if name in ["no_face", "unknown"]:
        return {"success": False, "message": "Face not recognized"}

    if not can_process(name):
        return {"success": True, "message": "duplicate ignored", "name": name}
    if not is_real_face(img):
        return {"success": False, "message": "Spoof detected (fake face)"}

    db = next(get_db())

    # get last record for this user
    last_record = db.query(Attendance)\
        .filter(Attendance.name == name)\
        .order_by(Attendance.timestamp.desc())\
        .first()

    # determine state
    if last_record is None or last_record.status == "OUT":
        status = "IN"
    else:
        status = "OUT"

    record = Attendance(
        name=name,
        status=status
    )

    db.add(record)
    db.commit()
    await manager.broadcast(
        {"name": name, "status": status, "timestamp": str(record.timestamp)}
    )

    return {
        "success": True,
        "name": name,
        "status": status
    }

