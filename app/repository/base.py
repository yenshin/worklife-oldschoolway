from sqlalchemy.orm import scoped_session
import uuid as uid
from app.tool.logger import Logger
from app.model.log import LogType, LogModel
from pprint import pprint

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _query(self, session, *_, **kwargs):
        filters = [getattr(self.model, k) == v for k, v in kwargs.items()]
        return session.query(self.model).filter(*filters)

    def get(self, session, *_, **kwargs):
        return self._query(session, **kwargs).one_or_none()

    def get_many(self, session, *_, **kwargs):
        return self._query(session, **kwargs).all()

    # INFO: This certainly not the best place for this fonction
    # certainly need to be discussed 
    def pushlog(self, session, type:LogType, msg:str, additionnalInfo:str):
        succeed = False
        log = Logger.GenerateLog(type, str, additionnalInfo)
        try:
            # INFO: uuid1 is not fully random and use timestand and host id
            # convenient for logs other things like that
            log.external_id = uid.uuid1()            
            session.add(log)
            session.commit()
            succeed = True
        except Exception as e:
            session.rollback()
            # log in stdout, with time I should log in file, with the possibility of
            # pushing them in the db            
            logErrL = Logger.GenerateLog(LogType.ERROR, "can't pushlog", log.ToString())
            pprint(logErrL)
        finally:
            session.close()
            return succeed

    def create(self, session, obj_in):
        succeed = False
        try:
            obj_in.external_id = uid.uuid4()
            session.add(obj_in)
            session.commit()
            succeed = True
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + obj_in.ToString()
            self.pushlog(session, LogType.ERROR, "create failed", additionnalInfo)            
        finally:
            session.close()
            return succeed
