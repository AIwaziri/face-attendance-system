from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    embedding = Column(LargeBinary)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)