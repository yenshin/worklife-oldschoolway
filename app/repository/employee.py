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
    
    def _convert_representation_to_model(self, representation:EmployeeBase) -> EmployeeModel:
        model = super(_EmployeeRepository, self)._convert_representation_to_model(representation)
        model.email = representation.email 
        model.first_name = representation.first_name 
        model.last_name = representation.last_name 
        return model     
    
    def get_employee(self, session, id):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_id(session, id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
        
    def get_employee_in_vacation(self, session, max_entry):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_id(session, id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
    
    def get_vacation_of_employee(self, session, id):
        # toReturn = None
        # session.expire_on_commit = False
        # try:
        #     toReturn = self._get_repr_by_id(session, id)
        # except Exception as e:
        #     additionnalInfo:str = str(e)
        #     # INFO: no clever message
        #     Logger.Pushlog(session, LogType.ERROR.value, "get_employee failed", additionnalInfo)            
        # finally:
        #     session.expire_on_commit = True
        #     return toReturn
        raise NotImplementedError
        
    def add_employee(self, session, representation:EmployeeBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = self._convert_representation_to_model(representation)            
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
