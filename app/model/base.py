import uuid as uid
import enum

from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import as_declarative


class CustomUUID(postgresql.UUID):
    python_type = uid.UUID


@as_declarative()
class BaseModel:
    internal_id = Column(postgresql.INTEGER, primary_key = True, unique = True, index = True)
    external_id = Column(CustomUUID(as_uuid=True), index=True, default=uid.uuid4)

    def ToDict(self):
        return {
            "internal_id" : self.internal_id,
            "external_id" : self.external_id              
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

