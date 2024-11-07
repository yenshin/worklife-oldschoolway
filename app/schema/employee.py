from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    first_name: str
    last_name: str
