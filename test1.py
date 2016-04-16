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
treatment_plan={
	'data':{
   "type": "treatment_plans",
   'attributes':{
   "title": "Treating Ail Cows",
   "body": {
      "head": "86937ab-9840-4c5d-b29f-cee613743676",
      "81c64ff9-c354-4fc9-b8d1-dd1a3986fed8": {
         "wait": "0",
         "description": "Euthanize immediately",
         "icon": "http://example.com/euthanize.jpg",
         "children": []
      },
      "d1ccebc3-48b1-45af-9075-d33f64e26e9d": {
         "wait": "0",
         "description": "Morbund or unfit for slaughter",
         "icon": "http://example.com/moribund.jpg",
         "children": ["81c64ff9-c354-4fc9-b8d1-dd1a3986fed8"]
      },
      "a388a993-a4ee-40b5-8629-3b21e29c480e": {
         "wait": "0",
         "description": "No response to treatment, condition declining",
         "icon": "http://example.com/no_response_to_treatment.jpg",
         "children": ["81c64ff9-c354-4fc9-b8d1-dd1a3986fed8"]
      },
      "d4430ee2-f33e-4798-bbd4-fdda82cbc665": {
         "wait": "0",
         "description": "Continue treatment, return animal to group",
         "icon": "http://example.com/continue_treatment_and_return.jpg",
         "children": []
      },
      "9cbe298c-660f-4a88-a43b-36fe0ae0c47c": {
         "wait": "0",
         "description": "Positive response to treatment, condition improves",
         "icon": "http://example.com/positive_response_to_treatment.jpg",
         "children": ["d4430ee2-f33e-4798-bbd4-fdda82cbc665"]
      },
      "e0915e62-c2e5-442b-90d7-f040952169b0": {
         "wait": "48",
         "description": "Separated for treatment or observation",
         "icon": "http://example.com/separated.jpg",
         "children": ["a388a993-a4ee-40b5-8629-3b21e29c480e", "9cbe298c-660f-4a88-a43b-36fe0ae0c47c"]
      },
      "59811a40-c9e8-4bb4-830a-e477df714f75": {
         "wait": "0",
         "description": "Send for slaughter",
         "icon": "http://example.com/send_for_slaughter.jpg",
         "children": []
      },
      "8b0f1293-4e45-4971-9aa0-ac7b2ae70154": {
         "wait": "0",
         "description": "No medications on board, fit for transport",
         "icon": "http://example.com/no_med_transportable.jpg",
         "children": ["59811a40-c9e8-4bb4-830a-e477df714f75"]
      },
      "648f01bf-8398-4d5d-bcf0-bea6bcc0b436": {
         "wait": "0",
         "description": "Unfit for transport",
         "icon": "http://example.com/untransportable.jpg",
         "children": []
      },
      "86937ab-9840-4c5d-b29f-cee613743676": {
         "wait": "0",
         "description": "head",
         "icon": "null",
         "children": ["d1ccebc3-48b1-45af-9075-d33f64e26e9d", "e0915e62-c2e5-442b-90d7-f040952169b0", "8b0f1293-4e45-4971-9aa0-ac7b2ae70154", "648f01bf-8398-4d5d-bcf0-bea6bcc0b436"]
      }
      }
   }
}
}
tp_post = requests.post("{url}/treatment_plans".format(url=base_url), headers=auth, json=treatment_plan);
print tp_post.status_code

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









