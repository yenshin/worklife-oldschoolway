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
    global url
    global head
    global employee001uuid
    global employee001mail
    global employee002uuid
    global employee002mail
    adduserurl = url + "/employee/"
    
    data = {
        "email": employee001mail,
        "first_name": "Bob",
        "last_name": "Bob"
    }
    employee = json.dumps(data)
    response = requests.post(url, data = employee)
    assert response.status_code == 404

    response = requests.post(adduserurl, data = employee)
    assert response.status_code == 405

    # INFO: add valid user with no external_id
    response = requests.put(adduserurl, headers = head, data = employee)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert str(employee001uuid) != contentReponse["external_id"]    

    # INFO: ensure no user with existing uuid
    tmpuuid = contentReponse["external_id"]
    getuserurl = adduserurl + str(employee001uuid)
    response = requests.get(getuserurl)
    contentReponse = json.loads(response.content)
    assert response.status_code == 400    
    employee001uuid = uuid.UUID(tmpuuid)

    # INFO: user previously added is correctly getted
    getuserurl = adduserurl + str(employee001uuid)
    response = requests.get(getuserurl)
    contentReponse = json.loads(response.content)
    assert response.status_code == 200
    assert contentReponse["external_id"] == str(employee001uuid)
    assert contentReponse["email"] == employee001mail

    # INFO: try to add new user but mail is already registered
    data["external_id"] = str(employee002uuid)
    employee = json.dumps(data)
    response = requests.put(adduserurl, data = employee)
    assert response.status_code == 400

    # INFO: fix the email add second user
    data["email"] = employee002mail
    employee = json.dumps(data)
    response = requests.put(adduserurl, data = employee)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert contentReponse["external_id"] == str(employee002uuid)
    assert contentReponse["email"] == employee002mail
    
    