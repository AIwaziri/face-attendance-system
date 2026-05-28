from fastapi import APIRouter, Depends
from sqlalchemy import desc

from ..db import get_db
from ..models import Attendance
from ..auth_deps import get_current_user


router = APIRouter()


@router.get("/")
def get_attendance(db=Depends(get_db), user=Depends(get_current_user)):

    query = db.query(Attendance)

    # 🔐 ROLE LOGIC
    if user.role != "admin":
        query = query.filter(Attendance.user_id == user.id)

    records = query.order_by(desc(Attendance.timestamp)).all()

    return [
        {
            "name": r.name,
            "status": r.status,
            "timestamp": str(r.timestamp)
        }
        for r in records
    ]