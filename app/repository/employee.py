from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
    
    def get_by_external_id(self, session, employee_id):
        return self.query(session).filter(self.model.external_id == employee_id)
    
    def add_employee(self, session, email, first_name, last_name):
        employee = EmployeeModel()
        employee.email = email
        employee.first_name = first_name
        employee.last_name = last_name
        return self.create(session, employee)
            

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
