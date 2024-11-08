from sqlalchemy.orm import scoped_session
import uuid as uid
from app.tool.logger import Logger
from app.model.log import LogType


class BaseRepository:    
    def __init__(self, model):
        self.model = model
        self._modelType = None
        self._representationType = None

    def _convert_model_to_representation(self, model):
        representation = self._representationType()
        representation.external_id = model.external_id
        return representation

        
    def _get_by_external_id(self, session, external_id):
        toReturn = None
        try:
            toReturn = session.query(self._modelType). \
                filter_by(external_id=external_id).\
                first()
            session.commit()
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + external_id
            Logger.Pushlog(session, LogType.ERROR.value, "get_one failed", additionnalInfo)            
        finally:
            session.close()
            return toReturn

    def _get_repr_by_external_id(self, session, external_id):
        dbObj = self._get_by_external_id(session, external_id)
        if dbObj != None:
            return self._convert_model_to_representation(dbObj)
        return None
    

    def create(self, session, obj_in):
        succeed = False
        try:
            if (obj_in.external_id == None):
                obj_in.external_id = uid.uuid4()
            session.add(obj_in)
            session.commit()
            succeed = True
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + obj_in.ToString()
            Logger.Pushlog(session, LogType.ERROR.value, "create failed", additionnalInfo)            
        finally:
            session.close()
            return succeed
