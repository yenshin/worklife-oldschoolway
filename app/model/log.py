from sqlalchemy import Column, Enum
from sqlalchemy.dialects import postgresql as pgs
from .base import BaseModel, LogType

# INFO: I put log in the sql db maybe in another kind of DB 
# imo logs should be not permenant.
# it's debatable depending of the use cae
class LogModel(BaseModel):
    __tablename__ = "employee"
    log_type = Column(Enum(LogType), index=True)
    prefix = Column(pgs.TEXT)
    msg = Column(pgs.TEXT)
    additionnal_info = Column(pgs.TEXT)

    def ToDict(self):
        dict = super().ToDict()
        dict["log_type"] = self.log_type
        dict["prefix"] = self.prefix
        dict["msg"] = self.msg
        dict["additionnal_info"] = self.additionnal_info
        return dict
