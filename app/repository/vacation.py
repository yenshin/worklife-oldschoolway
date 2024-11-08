from app.model import EmployeeVacationModel
from app.repository.base import BaseRepository
from app.schema import EmployeeVacationBase
from app.model.log import LogType
from app.tool.logger import Logger


class _EmployeeVacationRepository(BaseRepository):
    
    def __init__(self, model):
        super(model)
        self._modelType = EmployeeVacationModel
        self._representationType = EmployeeVacationBase

    def _convert_model_to_representation(self, model:EmployeeVacationModel) -> EmployeeVacationBase:
        representation = super(_EmployeeVacationRepository, self)._convert_model_to_representation(model)
        representation.user_id = model.user_id 
        representation.vacation_type = model.vacation_type 
        representation.start_date = model.start_date 
        representation.end_date = model.end_date 
        return representation 

    def _convert_representation_to_model(self, representation:EmployeeVacationBase) -> EmployeeVacationModel:
        model = super(_EmployeeVacationRepository, self)._convert_representation_to_model(representation)
        model.user_id = representation.user_id 
        model.vacation_type = representation.vacation_type 
        model.start_date = representation.start_date 
        model.end_date = representation.end_date 
        return model      

    def get_vacation(self, session, id):
        toReturn = None
        session.expire_on_commit = False
        try:
            toReturn = self._get_repr_by_id(session, id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "get_vacation failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
        
    def get_vacations(self, session):
        # toReturn = None
        # session.expire_on_commit = False
        # try:
        #     toReturn = self._get_repr_by_id(session, id)
        # except Exception as e:
        #     additionnalInfo:str = str(e)
        #     # INFO: no clever message
        #     Logger.Pushlog(session, LogType.ERROR.value, "get_vacation failed", additionnalInfo)            
        # finally:
        #     session.expire_on_commit = True
        #     return toReturn
        raise NotImplementedError()
        
    def add_vacation(self, session, representation:EmployeeVacationBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = self._convert_representation_to_model(representation)          
            if self.create(session, dbObj):
                toReturn = self._convert_model_to_representation(dbObj)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "add_vacation failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn

    def update_vacation(self, session, representation:EmployeeVacationBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            dbObj = self._convert_representation_to_model(representation)          
            if self.update(session, dbObj):
                toReturn = self._convert_model_to_representation(dbObj)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "update_vacation failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn

    def delete_vacation(self, session, vacation_id):
        toReturn = None
        session.expire_on_commit = False
        try:
            self.delete(session, vacation_id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            Logger.Pushlog(session, LogType.ERROR.value, "delete_vacation failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
EmployeeVacationRepository = _EmployeeVacationRepository(model=EmployeeVacationModel)