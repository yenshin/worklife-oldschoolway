from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pgs
from .base import BaseModel
from .employee_team import EmployeeTeamModel

class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    team_id = Column(pgs.INTEGER, ForeignKey(EmployeeTeamModel.id), index=True)    
    email = Column(pgs.VARCHAR(255), unique = True, index=True)
    first_name = Column(pgs.VARCHAR(255))
    last_name = Column(pgs.VARCHAR(255))

    def ToDict(self):
        dict = super().ToDict()
        dict["team_id"] = self.team_id
        dict["email"] = self.email
        dict["first_name"] = self.first_name
        dict["last_name"] = self.last_name
        return dict
