# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, make_response
from functools import wraps
import json
import requests

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'my precious'
base_url = 'http://localhost:10200/v1'
#base_url = 'https://katys-care-api.herokuapp.com/v1'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            
            return redirect(url_for('login'))
    return wrap


# use decorators to link the function to a url
@app.route('/')
#@login_required
def home():
    return render_template('index.html')  # render a template

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
            if login_status.status_code == 200:
                token = json.loads(login_status.text)['data']['id']
                session['token'] = token
                return redirect(url_for('home'))
            else:
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
    session.pop('token', None)
    return redirect(url_for('home'))

# route for handling displaying treatment plans list
@app.route('/treatment_plans')
def treatmentplan():
    r = open('plan.json')
    raw = json.dumps(r.read())
    return render_template('treatmentplan.html',data=raw)

# route for handling displaying list of cows
@app.route('/cows')
def cowList():
    return render_template('cows_list.html')

# route for handling displaying list of farms
@app.route('/farms')
def farmList():
    return "farms list"

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)