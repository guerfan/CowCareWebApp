import json
import requests
from flask import Flask, session
import pprint

base_url = 'http://localhost:10200/v1'
data={}
data['email']='allen@example.com'
data['password']='allen'
login_status = requests.post("{url}/token?include=user".format(url=base_url), json=data)
token = json.loads(login_status.text)['data']['id']
auth = {}
auth['Authorization']=token

##Setting vet's farm
# farm = {
# 	'data':{
# 		'type':'farms',
# 		'attributes':{
# 			'name':'farm3'
# 		},
# 		'relationships':{
# 			'veterinarian':
# 				{'data': [{
# 					'type':'users',
# 					'id': data['email']}]
# 				}
# 		}
# 	}
# }
# farm_status = requests.post("{url}/farms".format(url=base_url), json = farm, headers = auth)
# print farm_status
# farm_request = requests.get("{url}/farms".format(url=base_url), headers = auth)
# print farm_status.text
#print(json.dumps(json.loads(farm_request.text),indent = 4, sort_keys=True))

##Getting specific vet's farms
# farm_request = requests.get("{url}/users/{id}?include=vet_for".format(url=base_url, id=data['email']), headers=auth)
# print farm_request.text

farm_cow_request = requests.get("{url}/farms/{id}?include=calves".format(url=base_url, id='1ph5f'), headers=auth)
print farm_cow_request.text