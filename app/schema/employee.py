from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: Optional[UUID] = Field(None, description="the id to communicate from the client. can be set by the client")
    email: str = Field("xxx@xxx.com", description="")
    first_name: str = Field("John", description="")
    last_name: str = Field("Doe", description="")
