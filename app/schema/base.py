from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

class BaseRepresentation(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    external_id: Optional[UUID] = Field(None, description="the id to communicate from the client. can be set by the client")
