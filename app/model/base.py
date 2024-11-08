import uuid as uid
import enum

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import as_declarative


class CustomUUID(postgresql.UUID):
    python_type = uid.UUID


@as_declarative()
class BaseModel:
    # INFO: we use internal id for fast DB lookup and 
    # external id is when the system is distributed
    id = Column(CustomUUID(as_uuid=True), primary_key = True, index=True, default=uid.uuid4)

    def ToDict(self):
        return {
            "id" : self.id              
        }
    
    def ToString(self):
        return str(self.ToDict())
    
    def __repr__(self):
        return self.ToString()

class VacationType(enum.Enum):
    UnpaidLeave = 'UnpaidLeave'
    PaidLeave = 'PaidLeave'

    
class LogType(enum.Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICALSECURITY = 'CRITICALSECURITY'

