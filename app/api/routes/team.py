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
from app.repository import EmployeeTeamRepository
from app.schema import EmployeeTeamBase

router = APIRouter()

from app.model.log import LogType
from app.tool.logger import Logger

def __checkResponse(session: Session, response: Response, representation : EmployeeTeamBase):
    # INFO: status code is debatable
    if representation == None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    # INFO: I do not modify the status code to avoid giving information about server error    
    elif type(representation) != EmployeeTeamBase:
        Logger.Pushlog(session, LogType.CRITICALSECURITY.value, "Programmation error?, exposed value isn't what we expected")
        #response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        representation = None
    return representation
        

@router.get("/{id}", response_model=Optional[EmployeeTeamBase], status_code=200)
def get_team(id: UUID, response: Response, session: Session = Depends(get_db)):
    # # INFO: no oneliner to be benefit from VSCode remote debugger
    # INFO: no oneliner to be benefit from VSCode remote debugger
    representation = EmployeeTeamRepository.get_team(session, id)
    representation = __checkResponse(session, response, representation)
    return representation


@router.put("/", response_model=Optional[EmployeeTeamBase], status_code=201)
def add_employee(team:EmployeeTeamBase, response: Response, session: Session = Depends(get_db)):
    representation = EmployeeTeamRepository.add_team(session, team)
    representation = __checkResponse(session, response, representation)
    return representation
