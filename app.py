# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, make_response
from functools import wraps
import json
import requests
import uuid

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'  
# base_url = 'http://localhost:10200/v1'
base_url = 'https://katys-care-api.herokuapp.com/v1'


# use decorators to link the function to a url
@app.route('/')
#@login_required
def home():
    if 'token' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['action'] == 'Login':
            data ={}
            data['email']=request.form['username']
            data['password']=request.form['password']
            json_data = json.dumps(data)
            login_status = requests.post("{url}/token?include=user".format(url=base_url), json=data)
            if login_status.status_code in [200,201]:
                token = json.loads(login_status.text)['data']['id']
                session['token'] = token
                session['id'] = data['email']
                return redirect(url_for('home'))
            else:
                print login_status.status_code
                error = 'Invalid Credentials. Please try again.'
        elif request.form['action'] == 'Register':
                return redirect(url_for('register'))
    return render_template('login.html', error=error)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    error = None
    if request.method == "POST":
            data ={
                "data":{
                    "type": "users",
                    "attributes": {
                        "email": request.form['username'],
                        "password": request.form['password']
                    }
                }
            }
            register_status = requests.post("{url}/users".format(url=base_url), json=data)
            if register_status.status_code == 201:
                error = 'You are registered, please sign in.'
                return redirect(url_for('login'))
            else:
                error = 'Username is already used. Please try again.'
    return render_template('register.html', error=error)

# route for handling logout
@app.route('/logout')
# @login_required
def logout():
    delete_status = requests.delete
    session.pop('token', None)
    return redirect(url_for('login'))

# route for handling displaying treatment plans list
@app.route('/treatment_plans', methods = ['GET','POST','DELETE'])
def treatmentplanList():
    auth = {}
    if 'token' in session:
        auth['Authorization'] = session['token']
        treatment_plan_status = requests.get("{url}/users/{id}?include=treatment_plans".format(url=base_url, id=session['id']), headers=auth)
        if treatment_plan_status.status_code!= 200:
            return redirect(url_for('login'))
        json_treatment_list = json.loads(treatment_plan_status.text).get('included',[])
        json_treatment_list = [x for x in json_treatment_list if x["attributes"]["active"]]
        if request.method == "POST":
            new_treatment_attributes = request.get_json()
            data ={
                'data':{
                    'type': 'treatment_plans',
                    'attributes':new_treatment_attributes
                }
            }
            new_treatment_added_status = requests.post("{url}/treatment_plans".format(url=base_url),headers=auth, json=data)
            #treatment_plan_status = requests.get("{url}/treatment_plans".format(url=base_url),headers=auth)
            treatment_plan_status = requests.get("{url}/users/{id}?include=treatment_plans".format(url=base_url, id=session['id']), headers=auth)
            if treatment_plan_status.status_code != 200:
                return redirect(url_for('login'))
            #json_treatment_list = json.loads(treatment_plan_status.text)['data']
            json_treatment_list = json.loads(treatment_plan_status.text).get('included', [])
            json_treatment_list = [x for x in json_treatment_list if x["attributes"]["active"]]
            return render_template('treatment_list.html', treatment=json_treatment_list)
        if request.method == "DELETE":
            delete_json = request.get_json();
            treatment_id = delete_json['id'];
            data={
            'data':{
                    'type': 'treatment_plans',
                    'attributes':delete_json
                }
            }
            delete_json_status = requests.delete("{url}/treatment_plans/{id}".format(url=base_url, id=treatment_id),headers=auth, json =data)
            print delete_json_status.text;
    else:
        return redirect(url_for('login'))
    return render_template('treatment_list.html', treatment=json_treatment_list)

@app.route('/treatment_plans/<treatmentid>', methods = ['GET','POST'])
def treatmentplan(treatmentid):
    auth = {}
    if 'token' in session:
        auth['Authorization'] = session['token']
        treatment_plan_status = requests.get("{url}/treatment_plans/{id}".format(url=base_url, id = treatmentid),headers =auth)
        if treatment_plan_status.status_code!=200:
            return redirect(url_for('login'))
        id_treatment_plan = json.loads(treatment_plan_status.text)['data']['attributes']
        if request.method == "POST":
            updated_attributes = request.get_json()
            updated_plan ={
                'data':{
                    'type':'treatment_plans',
                    'attributes':updated_attributes
                }
            }
            update_plan_status = requests.patch("{url}/treatment_plans/{treatmentid}".format(url=base_url, treatmentid=treatmentid), headers=auth, json=updated_plan);
    return render_template('treatmentplan.html',data = json.dumps(id_treatment_plan))

# str(uuid.uuid4())

# route for handling displaying list of cows
@app.route('/calves')
def cowList():
    auth = {}
    if 'token' in session:
        auth['Authorization'] = session['token']
        calves_list_status = requests.get("{url}/calves".format(url=base_url),headers = auth)
        cows = json.loads(calves_list_status.text)['data']
    else:
        return redirect(url_for('login'))
    return render_template('cows_list.html',cows = cows)
    # return calves_list_status.text

@app.route('/<farm_id>')
def farms_cows(farm_id):
    auth = {}
    if 'token' in session:
        auth['Authorization'] = session['token']
        calves_list_status = requests.get("{url}/farms/{farm_id}?include=calves".format(url=base_url, farm_id=farm_id),headers = auth)
        cows = json.loads(calves_list_status.text).get('included',[])

    else:
        return redirect(url_for('login'))
    return render_template('cows_list.html',cows = cows)
    # return calves_list_status.text



# route for handling displaying list of farms
@app.route('/farms')
def farmList():
    auth = {}
    if 'token' in session:
        auth['Authorization'] = session['token']
        farm_list_status = requests.get("{url}/users/{id}?include=vet_for".format(url=base_url, id=session['id']), headers=auth)   
        farms = json.loads(farm_list_status.text).get('included', [])
    
        farm_cows = requests.get("{url}/calves".format(url=base_url),headers = auth)
    else:
        return redirect(url_for('login'))
    return render_template('farms_list.html', farms=farms)


    
    #return render_template('farms_list.html', data=json.dumps(farm_list_status.text))




@app.route('/addfarms', methods=['GET', 'POST'])
def farmListAdd():
    auth = {}
    if session.has_key('token') == True:
        auth['Authorization'] = session['token']
        if request.method == "POST":
            farm = {
                'data':{
                    'type':'farms',
                    'attributes':{
                        'name':request.form['farmname'],
                    },
                    'relationships':{
                        'veterinarian':
                            {'data': [{
                                'type':'users',
                                'id': session['id']}]
                            }
                    }
                }
            }
            farm_status = requests.post("{url}/farms".format(url=base_url), json=farm, headers=auth)
            if farm_status.status_code == 201:
                error = 'You are registered, please sign in.'
                return redirect(url_for('farmList'))
            else:
                error = 'Farm is already existed. Please try again.'
    else:
        return redirect(url_for('login'))
    return render_template('farms_list_add.html')

@app.route('/addcalves', methods=['GET', 'POST'])
def calvesListAdd():
    auth = {}
    if session.has_key('token') == True:
        auth['Authorization'] = session['token']
        if request.method == "POST":
            farm_list_status = requests.get("{url}/users/{id}?include=vet_for".format(url=base_url, id=session['id']), headers=auth)   
            farms = json.loads(farm_list_status.text).get('included', [])
            farm_id = 0
            for farm in farms: 
                if farm['attributes']['name'] == request.form['farmname']:
                    farm_id = farm['attributes']['id']

            calf = {
                'data':{
                    'type':'calves',
                    'attributes':{
                        'name':request.form['calfname'],
                        'type':'calves',
                        'cid':request.form['cid']
                    },
                    'relationships':{
                        'farm':
                            {'data': {
                                'type':'farms',
                                'id': farm_id}
                            }
                    },
                    'treatment_plan': {
                        'data': {
                            'type': 'treatment_plans',
                            'id': ''
                        }
                    }
                }
            }
            calf_status = requests.post("{url}/calves".format(url=base_url), json = calf, headers = auth)
            print calf_status.text
            if calf_status == 201:
                error = 'You are registered, please sign in.'
                return redirect(url_for('calves'))
            else:
                error = 'Calf is already existed. Please try again.'
    else:
        return redirect(url_for('login'))
    return render_template('cows_list_add.html')




# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)