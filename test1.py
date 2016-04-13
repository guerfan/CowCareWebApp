import json
import requests
from flask import Flask, session
import pprint

base_url = 'http://localhost:10200/v1'
data={}
data['email']='test@test.com'
data['password']='test'
login_status = requests.post("{url}/token?include=user".format(url=base_url), json=data)
token = json.loads(login_status.text)['data']['id']
auth = {}
auth['Authorization']=token

# Post Treatment plan attemp
json = {
	'head':'headache'
}
treatment_plan={
	'data':{
		'type':'treatment_plans',
		'attributes':{'title':'Treatmentment 1',
		'body':json}
	}
}
tp_post = requests.post("{url}/treatment_plans".format(url=base_url), headers=auth, json=treatment_plan);
print tp_post.text

# # Retrive treatment plan
# tp_status = requests.get("{url}/treatment_plans".format(url=base_url),headers = auth)
# print tp_status.text

# ##Setting vet's farm
# farm = {
# 	'data':{
# 		'type':'farms',
# 		'attributes':{
# 			'name':'farm3'
# 		},
# 		'relationships':{
# 			'veterinarian':
#  				{'data': [{
# 					'type':'users',
# 					'id': data['email']}]
# 				}
# 		}
# 	}
# }
# farm_status = requests.post("{url}/farms".format(url=base_url), json = farm, headers = auth)
# print farm_status

# #farm request
# farm_request = requests.get("{url}/farms".format(url=base_url), headers = auth)
# print farm_request.text
# print(json.dumps(json.loads(farm_request.text),indent = 4, sort_keys=True))

# #Getting specific vet's farms
# farm_request = requests.get("{url}/users/{id}?include=vet_for".format(url=base_url, id=data['email']), headers=auth)
# print farm_request.text

##Request cows
# farm_cow_request = requests.get("{url}/farms/{id}?include=calves".format(url=base_url, id='1ph5f'), headers=auth)
# cows = json.loads(farm_cow_request.text)['data']['relationships']['calves']['data']
# print cows
# print farm_cow_request.text

##Delete example
# delete_status = requests.delete("{url}/users/allen@example.com".format(url=base_url),json = token, headers = auth)
# print delete_status
# print delete_status.text









