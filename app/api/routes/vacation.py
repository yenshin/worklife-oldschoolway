from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import (
    Depends,
    APIRouter,
    Response,
    status    
)

from sqlalchemy.orm import Session
from app.repository import EmployeeVacationRepository
from app.schema import EmployeeVacationBase
from app.schema import EmployeeBase

from app.db.session import get_db

from app.model.log import LogType
from app.tool.logger import Logger

router = APIRouter()

def __checkIfVacationIsValid(begin: datetime, end: datetime):
    # INFO: date should not be set in the weekend
    if begin.weekday() > 5 or end.weekday() > 5:
        return False
    # begin == end is 1 day vacation
    if end < begin:
        return False    
    return True

def __checkEmploeeListResponse(session: Session, response: Response, employeeList : list[EmployeeBase]):
    # # INFO: status code is debatable
    # if representation == None:
    #     response.status_code = status.HTTP_400_BAD_REQUEST
    # # INFO: I do not modify the status code to avoid giving information about server error    
    # elif type(representation) != EmployeeVacationBase or \
    #     __checkIfVacationIsValid(representation.start_date, representation.end_date) == False:
    #     Logger.Pushlog(session, LogType.CRITICALSECURITY.value, "Programmation error?, exposed value isn't what we expected")
    #     #response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     representation = None
    # return representation
    return True

def __checkSingleResponse(session: Session, response: Response, representation : EmployeeVacationBase):
    # INFO: status code is debatable
    if representation == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    # INFO: I do not modify the status code to avoid giving information about server error    
    elif type(representation) != EmployeeVacationBase or \
        __checkIfVacationIsValid(representation.start_date, representation.end_date) == False:
        Logger.Pushlog(session, LogType.CRITICALSECURITY.value, "Programmation error?, exposed value isn't what we expected")
        #response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        representation = None
    return representation

def __checkMultipleResponse(session: Session, response: Response, representationList : list[EmployeeVacationBase]):
    for employee in representationList:
        if __checkSingleResponse(session, response, employee) == None:
            Logger.Pushlog(session, LogType.CRITICALSECURITY.value, "Programmation error?, coming from list (2 logs 1 here 1 for specific data)")
            return None
    return representationList


            
@router.get("/", response_model=Optional[EmployeeVacationBase], status_code=200)
def get_vacations(response: Response, session: Session = Depends(get_db)):
    # # INFO: no oneliner to be benefit from VSCode remote debugger
    # representation = EmployeeVacationRepository.get_vacations(session)
    # representation = __checkResponse(session, response, representation)
    # return representation
    raise NotImplementedError()

@router.get("/{id}", response_model=Optional[EmployeeVacationBase], status_code=200)
def get_vacation(id: UUID, response: Response, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeVacationRepository.get_vacation(session, id)
    representation = __checkSingleResponse(session, response, representation)
    return representation

@router.get("/employee/", response_model=Optional[list[UUID]], status_code=200)
def get_employee_in_vacation(response: Response, max_entry:int = 10, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeVacationRepository.get_employee_in_vacation(session, max_entry)
    representation = __checkSingleResponse(session, response, representation)
    return representation

@router.get("/employee/{id}", response_model=Optional[list[EmployeeVacationBase]], status_code=200)
def get_vacation_of_employee(id: UUID, response: Response, max_entry:int = 10, session: Session = Depends(get_db)):
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeVacationRepository.get_vacation_of_employee(session, id)
    representation = __checkMultipleResponse(session, response, representation)
    return representation

@router.put("/", response_model=Optional[EmployeeVacationBase], status_code=201)
def add_vacation(vacation:EmployeeVacationBase, response: Response, session: Session = Depends(get_db)):
    if __checkIfVacationIsValid(vacation.start_date, vacation.end_date):
        representation = EmployeeVacationRepository.add_vacation(session, vacation)
        representation = __checkSingleResponse(session, response, representation)
        return representation
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

@router.post("/{id}", response_model=Optional[EmployeeVacationBase], status_code=200)
def update_vacations(id: UUID, vacation:EmployeeVacationBase, response: Response, session: Session = Depends(get_db)):    
    if __checkIfVacationIsValid(vacation.start_date, vacation.end_date):
        representation = EmployeeVacationRepository.update_vacation(session, vacation)
        representation = __checkSingleResponse(session, response, representation)
        return representation
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    
@router.delete("/{id}", response_model=Optional[EmployeeVacationBase], status_code=200)
def delete_vacations(id: UUID, response: Response, session: Session = Depends(get_db)):
    if EmployeeVacationRepository.delete_vacation(session, id) == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
    

