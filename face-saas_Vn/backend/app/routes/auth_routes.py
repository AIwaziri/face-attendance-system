from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import User
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Auth"])


# ----------------------------
# REGISTER
# ----------------------------

@router.post("/register")
def register(name: str, password: str, role: str = "employee", db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        name=name,
        password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


# ----------------------------
# LOGIN
# ----------------------------

@router.post("/login")
def login(name: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.name == name).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"user_id": user.id, "role": user.role}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }