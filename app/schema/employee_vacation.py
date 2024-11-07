from pydantic import BaseModel, ConfigDict


class EmployeeVacationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: str
    employee_id: str
    vacation_type: str
    start_data: str
    end_data: str
