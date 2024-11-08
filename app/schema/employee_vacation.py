from pydantic import Field
from .base import BaseRepresentation

class EmployeeVacationBase(BaseRepresentation):
    vacation_type: str = Field("vacation type", description="can be paid or not")
    start_data: str = Field("start data", description="")
    end_data: str = Field("start data", description="")
