from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pgs
from .base import BaseModel, VacationType
from .employee import EmployeeModel

class EmployeeVacationModel(BaseModel):
    __tablename__ = "employee_vacation"
    # INFO: because in this project we are not really distributed we use the internal_id
    # as fk. it should be enough. debatable depending of the use case
    user_id = Column(pgs.INTEGER, ForeignKey(EmployeeModel.internal_id), index=True)    
    vacation_type = Column(pgs.ENUM(VacationType, name="vacationtype", create_type=False), index = True)
    start_data = Column(pgs.DATE, index = True)
    end_date = Column(pgs.DATE, index = True)
