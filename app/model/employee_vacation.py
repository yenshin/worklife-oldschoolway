from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pgs
from .base import BaseModel, VacationType
from .employee import EmployeeModel

class EmployeeVacationModel(BaseModel):
    __tablename__ = "employee_vacation"
    user_id = Column(pgs.INTEGER, ForeignKey(EmployeeModel.id), index=True)    
    vacation_type = Column(pgs.ENUM(VacationType, name="vacationtype", create_type=False), index = True)
    # INFO: pgsql doesn't have a datetime column, so use timestamp    
    start_date = Column(pgs.TIMESTAMP, index = True)
    end_date = Column(pgs.TIMESTAMP, index = True)
