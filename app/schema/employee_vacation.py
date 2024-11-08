from pydantic import Field
from typing import Optional
from .base import BaseRepresentation
from uuid import UUID
from datetime import datetime

class EmployeeVacationBase(BaseRepresentation):
    user_id: Optional[UUID] = Field(UUID(int=0), description="the user id")
    vacation_type: str = Field("vacation type", description="can be paid or not")
    start_date: datetime = Field("start data", description="start day of vacation")
    end_date: datetime = Field("end data", description="last day of vacation (included)")
