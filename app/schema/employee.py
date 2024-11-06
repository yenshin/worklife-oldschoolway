from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
