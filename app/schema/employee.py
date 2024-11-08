from pydantic import Field
from .base import BaseRepresentation

class EmployeeBase(BaseRepresentation):
    email: str = Field("xxx@xxx.com", description="")
    first_name: str = Field("John", description="")
    last_name: str = Field("Doe", description="")
