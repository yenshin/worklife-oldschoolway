from pydantic import Field
from .base import BaseRepresentation

class EmployeeTeamBase(BaseRepresentation):
    team_name: str = Field("coffee", description="")
