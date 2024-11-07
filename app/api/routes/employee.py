from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema import EmployeeBase

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(employee_id: UUID, session: Session = Depends(get_db)):
    return EmployeeRepository.get_by_external_id(session=session, external_id=employee_id)

@router.put("/", response_model=Optional[EmployeeBase])
def add_employee(employee:EmployeeBase, response:Response, session: Session = Depends(get_db), ):
    employeeRepo = EmployeeRepository.add_employee(session, employee)
    response.body = employeeRepo
    response.status_code = status.HTTP_201_CREATED
