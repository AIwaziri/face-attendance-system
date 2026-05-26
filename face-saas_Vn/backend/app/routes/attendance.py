from fastapi import APIRouter
from ..db import get_db
from ..models import Attendance

router = APIRouter()


@router.get("/")
def get_attendance():
    db = next(get_db())
    records = db.query(Attendance).all()

    return [
        {
            "name": r.name,
            "status": r.status,
            "timestamp": str(r.timestamp)
        }
        for r in records
    ]