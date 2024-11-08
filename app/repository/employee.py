from app.model import EmployeeModel
from app.repository.base import BaseRepository
from app.schema import EmployeeBase
from app.tool.logger import Logger
from app.model.log import LogType
class _EmployeeRepository(BaseRepository):
    
    def get_by_external_id(self, session, employee_id):
        session.expire_on_commit = False
        queryResult = None
        try:
            queryResult = self.get_one(session, EmployeeModel, employee_id)
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            self.pushlog(session, LogType.ERROR.value, "add_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return queryResult
    
    def add_employee(self, session, employeebase:EmployeeBase):
        toReturn = None
        session.expire_on_commit = False
        try:
            employee = EmployeeModel()
            employee.email = employeebase.email
            employee.first_name = employeebase.first_name
            employee.last_name = employeebase.last_name
            employee.external_id = employeebase.external_id
            if self.create(session, employee):
                toReturn = EmployeeBase()
                toReturn.external_id = employee.external_id
                toReturn.email = employee.email
                toReturn.first_name = employee.first_name
                toReturn.last_name = employee.last_name
        except Exception as e:
            additionnalInfo:str = str(e)
            # INFO: no clever message
            self.pushlog(session, LogType.ERROR.value, "add_employee failed", additionnalInfo)            
        finally:
            session.expire_on_commit = True
            return toReturn
            

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
