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
@login_required
def home():
    return render_template('index.html')  # render a template
   


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
 #       if (request.form['username'] != 'admin') \
 #               or request.form['password'] != 'admin':
 #           error = 'Invalid Credentials. Please try again.'
 #       else:
 #           session['logged_in'] = True
 #           flash('You were logged in.')
 #           return redirect(url_for('home'))
        data ={}
        username = request.form['username']
        password = request.form['password']
        data['email']=username
        data['password']=password
        json_data = json.dumps(data)
        login_status = requests.post("{url}/token?include=user".format(url=base_url), json=data)
        print login_status.status_code
#        print json_data
        if login_status.status_code == 200:
            token = json.loads(login_status.text)['data']['id']
            response = redirect(url_for('home'))
            response.set_cookie('token',value=token)
            session['logged_in'] = True
            return response
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)