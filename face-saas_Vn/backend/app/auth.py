from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

# 🔐 CONFIG
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# ✅ USE ARGON2 (modern + secure + no 72-byte issue)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ----------------------------
# PASSWORD SECURITY
# ----------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------
# JWT TOKEN
# ----------------------------

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)