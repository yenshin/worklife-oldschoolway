from app.model import EmployeeModel
from app.repository.base import BaseRepository
from app.schema import EmployeeBase
from app.model.log import LogType
from app.tool.logger import Logger

class _EmployeeRepository(BaseRepository):
    
    def __init__(self, model):
        super(model)
        self._modelType = EmployeeModel
        self._representationType = EmployeeBase
    
    def _convert_model_to_representation(self, model:EmployeeModel) -> EmployeeBase:
        representation = super(_EmployeeRepository, self)._convert_model_to_representation(model)
        representation.email = model.email
        representation.first_name = model.first_name
        representation.last_name = model.last_name
        return representation      
    
    def get_employee(self, session, external_id):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_external_id(session, external_id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
        
    def add_employee(self, session, employeebase:EmployeeBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = EmployeeModel()
            dbObj.email = employeebase.email
            dbObj.first_name = employeebase.first_name
            dbObj.last_name = employeebase.last_name
            # INFO: external_id can be updated in self.create
            dbObj.external_id = employeebase.external_id            
            if self.create(session, dbObj):                
                toReturn = self._convert_model_to_representation(dbObj)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "add_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
            

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
