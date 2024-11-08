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
from app.repository import EmployeeRepository
from app.schema import EmployeeBase

from app.model.log import LogType
from app.tool.logger import Logger

router = APIRouter()

def __checkResponse(session: Session, response: Response, representation : EmployeeBase):
    # INFO: status code is debatable
    if representation == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    # INFO: I do not modify the status code to avoid giving information about server error    
    elif type(representation) != EmployeeBase:
        Logger.Pushlog(session, LogType.CRITICALSECURITY.value, "Programmation error?, exposed value isn't what we expected")
        #response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        representation = None
    return representation
        
    

@router.get("/{id}", response_model=Optional[EmployeeBase], status_code=200)
def get_employee(id: UUID, response: Response, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeRepository.get_employee(session, id)
    representation = __checkResponse(session, response, representation)
    return representation

@router.put("/", response_model=Optional[EmployeeBase], status_code=201)
def add_team(employee:EmployeeBase, response: Response, session: Session = Depends(get_db)):
    representation = EmployeeRepository.add_employee(session, employee)
    representation = __checkResponse(session, response, representation)
    return representation

@router.get("/{id}", response_model=Optional[EmployeeBase], status_code=200)
def get_employee(id: UUID, response: Response, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeRepository.get_employee(session, id)
    representation = __checkResponse(session, response, representation)
    return representation
