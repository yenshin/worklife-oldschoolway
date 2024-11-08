from app.model import EmployeeTeamModel
from app.repository.base import BaseRepository
from app.schema import EmployeeTeamBase
from app.model.log import LogType
from app.tool.logger import Logger


class _EmployeeTeamRepository(BaseRepository):
    
    def __init__(self, model):
        super(model)
        self._modelType = EmployeeTeamModel
        self._representationType = EmployeeTeamBase

    def _convert_model_to_representation(self, model:EmployeeTeamModel) -> EmployeeTeamBase:
        representation = super(_EmployeeTeamRepository, self)._convert_model_to_representation(model)
        representation.team_name = model.team_name  
        return representation      

    def get_team(self, session, external_id):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_external_id(session, external_id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_team failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
        
    def add_team(self, session, employeebase:EmployeeTeamBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = EmployeeTeamModel()
            dbObj.team_name = employeebase.team_name 
            # INFO: external_id can be updated in self.create
            dbObj.external_id = employeebase.external_id                 
            if self.create(session, dbObj):
                toReturn = self._convert_model_to_representation(dbObj)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "add_team failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
EmployeeTeamRepository = _EmployeeTeamRepository(model=EmployeeTeamModel)