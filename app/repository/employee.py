from app.model import EmployeeModel
from app.repository.base import BaseRepository
from app.schema import EmployeeBase

class _EmployeeRepository(BaseRepository):
    
    def get_by_external_id(self, session, employee_id):
        return self.query(session).filter(self.model.external_id == employee_id)
    
    def add_employee(self, session, employeebase:EmployeeBase):
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
            return toReturn
        return None
            

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
