from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from datetime import datetime
from .db import Base


# 👤 USER (AUTH)
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="employee")
    embedding = Column(LargeBinary)


# 👥 EMPLOYEE
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    role = Column(String, default="staff")
    created_at = Column(DateTime, default=datetime.utcnow)


# 📊 ATTENDANCE
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)