from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Response,
    status    
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema import EmployeeBase

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase], status_code=200)
def get_employee(employee_id: UUID, response: Response, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    employeeRepo = EmployeeRepository.get_by_external_id(session, employee_id)
    if employeeRepo == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return employeeRepo

@router.put("/", response_model=Optional[EmployeeBase], status_code=201)
def add_employee(employee:EmployeeBase, response: Response, session: Session = Depends(get_db)):
    employeeRepo = EmployeeRepository.add_employee(session, employee)
    if employeeRepo == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return employeeRepo
