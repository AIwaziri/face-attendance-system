from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..models import Employee
from ..auth_deps import require_admin

router = APIRouter()

# 🔐 ADMIN ONLY - ADD EMPLOYEE
@router.post("/add")
def add_employee(name: str, role: str = "staff", admin=Depends(require_admin)):
    db = next(get_db())

    existing = db.query(Employee).filter(Employee.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Employee exists")

    emp = Employee(name=name, role=role)
    db.add(emp)
    db.commit()

    return {"message": "Employee added by admin"}


# 👥 ANY AUTH USER CAN VIEW
@router.get("/")
def get_employees():
    db = next(get_db())
    return db.query(Employee).all()


# 🔐 ADMIN ONLY - DELETE
@router.delete("/{emp_id}")
def delete_employee(emp_id: int, admin=Depends(require_admin)):
    db = next(get_db())

    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(emp)
    db.commit()

    return {"message": "Deleted by admin"}