import requests
import uuid
import json

# Define the API endpoint URL
url = 'http://localhost:8080/'
head= {'accept': 'application/json', 'Content-Type': 'application/json'}
employee001uuid = uuid.uuid4()
employee001mail = 'employee001' + employee001uuid.hex.upper()[0:6] + "@gmail.com"

employee002uuid = uuid.uuid4()
employee002mail = 'employee002' + employee002uuid.hex.upper()[0:6] + "@gmail.com"

def test_employee():
    adduserurl = url + "/employee/"
    
    employee = json.dumps({
        "email": employee001mail,
        "first_name": "Bob",
        "last_name": "Bob"
    })

    # employee = EmployeeBase()
    # employee.email = employee001mail
    # employee.first_name = employee001mail
    # employee.last_name = employee001mail

    response = requests.post(url, data = employee)
    assert response.status_code == 404

    response = requests.post(adduserurl, data = employee)
    assert response.status_code == 405

    response = requests.put(adduserurl, headers = head, data = employee)
    assert response.status_code == 201

    data = {
        "external_id": employee002uuid,
        "email": employee001mail,
        "first_name": "Bob",
        "last_name": "Bob",
    }
    response = requests.put(adduserurl, data = data)
    assert response.status_code == 400

    data["email"] = employee002mail
    response = requests.put(adduserurl, data = data)
    assert response.status_code == 201

