from fastapi import APIRouter, Depends
from sqlalchemy import func
from datetime import datetime, timedelta

from ..db import get_db
from ..models import Attendance
from ..auth_deps import require_admin
from fastapi import APIRouter


router = APIRouter()

# =========================
# DAILY STATS
# =========================
@router.get("/daily")
def daily_stats(user=Depends(require_admin)):
    db = next(get_db())

    today = datetime.utcnow().date()

    records = db.query(Attendance).filter(
        func.date(Attendance.timestamp) == today
    ).all()

    total = len(records)
    ins = len([r for r in records if r.status == "IN"])
    outs = len([r for r in records if r.status == "OUT"])

    return {
        "total": total,
        "in": ins,
        "out": outs
    }


# =========================
# WEEKLY TREND (for charts)
# =========================
@router.get("/weekly")
def weekly_stats(user=Depends(require_admin)):
    db = next(get_db())

    data = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)

        records = db.query(Attendance).filter(
            func.date(Attendance.timestamp) == day
        ).all()

        data.append({
            "date": str(day),
            "total": len(records)
        })

    return data