import requests
import json
# Create User

base_url = 'https://katys-care-api.herokuapp.com/v1'
"""
u = {
  "data":{
    "type": "users",
    "attributes": {
      "email": "allen@example.com",
      "password": "allen"
    }
  }
}
r = requests.post("{url}/users".format(url=base_url), json=u)

print r.status_code
print r.text
"""

# Get user token

t = {
	"email": "allen@example.com",
	"password": "allen"
}
r2 = requests.post("{url}/token?include=user".format(url=base_url), json=t)

# Get Treatment plan

token = json.loads(r2.text)['data']['id']
print token
headers = {'Authorization': token}
tp = requests.get("{url}/treatment_plans".format(url=base_url), headers=headers)


print tp.status_code
print tp.text





