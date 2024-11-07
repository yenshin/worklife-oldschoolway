from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects import postgresql as pgs
from .base import BaseModel


class EmployeeTeamModel(BaseModel):
    __tablename__ = "employee_team"
    team_name = Column(pgs.VARCHAR(255), unique = True, index=True)
