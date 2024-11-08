
from enum import Enum
import uuid as uid
import sys
import inspect
import os
from pprint import pprint

from app.model.log import LogModel, LogType



class Logger:

    @staticmethod
    def __GeneratePrefix():
        prefix = ""
        frame =  sys._getframe().f_back.f_back
        if (frame == None):
            prefix = "unknown[?: ?]"
        else:
            info = inspect.getframeinfo(frame)
            funcName = info.function
            fileName = os.path.basename(info.filename)
            lineNumber = info.lineno
            prefix = "%s[%s: %s]" % (str(fileName), str(funcName), str(lineNumber))
        return prefix

    @staticmethod
    def GenerateLog(logType: LogType, msg:str, additionnalInfo:str = "") -> LogModel:
        prefix = Logger.__GeneratePrefix()
        logModel = LogModel()
        logModel.log_type = logType
        logModel.prefix = prefix
        logModel.msg = msg
        logModel.additionnal_info = additionnalInfo

        return logModel

    @staticmethod
    def Pushlog(session, type:LogType, msg:str, additionnalInfo:str = ""):
        succeed = False
        log = Logger.GenerateLog(type, msg, additionnalInfo)
        try:
            # INFO: uuid1 is not fully random and use timestand and host id
            # convenient for logs other things like that
            log.external_id = uid.uuid1()            
            session.add(log)
            session.commit()
            succeed = True
        except Exception as e:
            session.rollback()
            additionnalInfo:str = str(e)
            additionnalInfo += "\n" + log.ToString()
            # log in stdout, with time I should log in file, with the possibility of
            # pushing them in the db            
            logErrL = Logger.GenerateLog(LogType.ERROR, "can't pushlog", additionnalInfo)
            pprint(logErrL)
        finally:
            session.close()
            return succeed