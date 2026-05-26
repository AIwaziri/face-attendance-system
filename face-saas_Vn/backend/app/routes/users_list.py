from fastapi import APIRouter
from ..db import get_db
from ..models import User

router = APIRouter()


@router.get("/")
def get_users():
    db = next(get_db())

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "name": u.name
        }
        for u in users
    ]