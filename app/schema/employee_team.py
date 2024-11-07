from pydantic import BaseModel, ConfigDict


class EmployeeTeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    team_name: str
