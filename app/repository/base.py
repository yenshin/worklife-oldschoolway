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
        representation.id = model.id
        return representation
    
    def _convert_representation_to_model(self, representation):
        model = self._modelType()
        # INFO: id can be by client or updated in self.create if None
        model.id = representation.id
        return model

        
    def _get_by_id(self, session, id):
        toReturn = None
        try:
            toReturn = session.query(self._modelType). \
                filter_by(id=id).\
                first()
            session.commit()
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + id
            Logger.Pushlog(session, LogType.ERROR.value, "get_one failed", additionnalInfo)            
        finally:
            session.close()
            return toReturn

    def _get_repr_by_id(self, session, id):
        dbObj = self._get_by_id(session, id)
        if dbObj != None:
            return self._convert_model_to_representation(dbObj)
        return None
    

    def create(self, session, obj_in):
        succeed = False
        try:
            if (obj_in.id == None):
                obj_in.id = uid.uuid4()
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
        
    def update(self, session, obj_in):
        toReturn = None
        try:
            toReturn = session.query(self._modelType). \
                filter_by(id=obj_in.id).\
                first()
            toReturn = obj_in
            session.commit()
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + obj_in.ToString()
            Logger.Pushlog(session, LogType.ERROR.value, "update failed", additionnalInfo)            
        finally:
            session.close()
            return toReturn
        
    def delete(self, session, id):
        toReturn = None
        try:
            toReturn = session.query(self._modelType). \
                filter_by(id=id).\
                delete()
            session.commit()
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + id
            Logger.Pushlog(session, LogType.ERROR.value, "delete failed", additionnalInfo)            
        finally:
            session.close()
            return toReturn

