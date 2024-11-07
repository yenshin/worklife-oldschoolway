
from enum import Enum
import uuid as uid
import sys
import inspect
import os

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
