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

    def _convert_representation_to_model(self, representation:EmployeeTeamBase) -> EmployeeTeamModel:
        model = super(_EmployeeTeamRepository, self)._convert_representation_to_model(representation)
        model.team_name = representation.team_name         
        return model  
    
    def get_team(self, session, id):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_id(session, id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_team failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
        
    def add_team(self, session, representation:EmployeeTeamBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = self._convert_representation_to_model(representation)
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