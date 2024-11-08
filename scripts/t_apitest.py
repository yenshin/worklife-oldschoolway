import requests
import uuid
import json
from app.model.base import VacationType
from datetime import datetime

# INFO: dirty hack to add app.model.base
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

# Define the API endpoint URL
url = 'http://localhost:8080/'
head= {'accept': 'application/json', 'Content-Type': 'application/json'}
employee001uuid = uuid.uuid4()
employee001mail = 'employee001' + employee001uuid.hex.upper()[0:6] + "@gmail.com"

employee002uuid = uuid.uuid4()
employee002mail = 'employee002' + employee002uuid.hex.upper()[0:6] + "@gmail.com"

team001uuid = uuid.uuid4()
team001name = 'team001' + team001uuid.hex.upper()[0:6]

team002uuid = uuid.uuid4()
team002name = 'team002' + team001uuid.hex.upper()[0:6]

vacation001uuid = uuid.uuid4()
vacation002uuid = uuid.uuid4()
vacation003uuid = uuid.uuid4()
vacation004uuid = uuid.uuid4()



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

    # INFO: add valid user with no id
    response = requests.put(adduserurl, headers = head, data = employee)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert str(employee001uuid) != contentReponse["id"]    

    # INFO: ensure no user with existing uuid
    tmpuuid = contentReponse["id"]
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
    assert contentReponse["id"] == str(employee001uuid)
    assert contentReponse["email"] == employee001mail

    # INFO: try to add new user but mail is already registered
    data["id"] = str(employee002uuid)
    employee = json.dumps(data)
    response = requests.put(adduserurl, data = employee)
    assert response.status_code == 400

    # INFO: fix the email add second user
    data["email"] = employee002mail
    employee = json.dumps(data)
    response = requests.put(adduserurl, data = employee)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert contentReponse["id"] == str(employee002uuid)
    assert contentReponse["email"] == employee002mail
    
def test_team():
    global url
    global head
    global team001uuid
    global team001name
    global team002uuid
    global team002name
    addteamurl = url + "/team/"

    data = {
        "team_name": team001name,
    }
    team = json.dumps(data)
    response = requests.post(url, data = team)
    assert response.status_code == 404

    # INFO: wrong route
    response = requests.post(addteamurl, data = team)
    assert response.status_code == 405

    # INFO: add valid team with no id
    response = requests.put(addteamurl, headers = head, data = team)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert str(team001uuid) != contentReponse["id"]    

    # INFO: ensure no user with existing uuid
    tmpuuid = contentReponse["id"]
    getteamurl = addteamurl + str(team001uuid)
    response = requests.get(getteamurl)
    contentReponse = json.loads(response.content)
    assert response.status_code == 400    
    team001uuid = uuid.UUID(tmpuuid)

    # INFO: user previously added is correctly getted
    getteamurl = addteamurl + str(team001uuid)
    response = requests.get(getteamurl)
    contentReponse = json.loads(response.content)
    assert response.status_code == 200
    assert contentReponse["id"] == str(team001uuid)
    assert contentReponse["team_name"] == team001name

    # INFO: try to add new team but name is already registered
    data["id"] = str(team002uuid)
    team = json.dumps(data)
    response = requests.put(addteamurl, data = team)
    assert response.status_code == 400

    # INFO: fix the email add second user
    data["team_name"] = team002name
    team = json.dumps(data)
    response = requests.put(addteamurl, data = team)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert contentReponse["id"] == str(team002uuid)
    assert contentReponse["team_name"] == team002name

def test_vacation():
    global url
    global head
    global employee001uuid
    global employee002uuid

    global vacation001uuid
    global vacation002uuid
    global vacation003uuid
    global vacation004uuid
    addvacationurl = url + "/vacation/"

    data = {
        "user_id": str(employee001uuid),
        "vacation_type": VacationType.PaidLeave.value,
        "start_date": datetime(2010,1,1).timestamp(),
        "end_date": datetime(2020,1,1).timestamp()
    }
    vacation = json.dumps(data)
    response = requests.post(url, data = vacation)
    assert response.status_code == 404

    # INFO: wrong route
    response = requests.post(addvacationurl, data = vacation)
    assert response.status_code == 405

    # INFO: add vacation team with no id
    response = requests.put(addvacationurl, headers = head, data = vacation)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert str(vacation001uuid) != contentReponse["id"]

    # INFO: remove vacation
    specificVacationUrl = addvacationurl + contentReponse["id"]    
    response = requests.delete(specificVacationUrl, headers = head)
    assert response.status_code == 200

    # INFO: add valid vacation with client id
    data["id"] = str(vacation001uuid)
    vacation = json.dumps(data)
    response = requests.put(addvacationurl, headers = head, data = vacation)
    assert response.status_code == 201
    contentReponse = json.loads(response.content)
    assert str(vacation001uuid) == contentReponse["id"]

    # INFO: update vacation with client id
    data["vacation_type"] = VacationType.UnpaidLeave.value
    specificVacationUrl = addvacationurl + data["id"]   
    vacation = json.dumps(data)
    response = requests.post(specificVacationUrl, headers = head, data = vacation)
    assert response.status_code == 200
    contentReponse = json.loads(response.content)
    assert str(vacation001uuid) == contentReponse["id"]
    assert data["vacation_type"] == contentReponse["vacation_type"]
