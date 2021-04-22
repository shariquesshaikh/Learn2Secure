from flask import Flask, render_template, request, flash, session, redirect, url_for
from pymongo import MongoClient
import uuid, os, bcrypt

app = Flask(__name__)

app.secret_key = 'n0T@talls1mpl3'

client = MongoClient(
    "mongodb+srv://l2s_user:ltos_yous3R@l2c.xzbms.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('l2c_db')
data = db.reg_users


# Default URL
@app.route('/')
def home():
    name = ''
    if session.get('logged_in'):
        name = session['name']
    return render_template('index.html', name = name)

# Registration Request
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'cpassword' in request.form:
        exist = data.find_one({'email': request.form['email']})
        if (exist is None):
            if (request.form['password'] == request.form['cpassword']):
                hashedpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                data.insert({'_id': uuid.uuid4().hex, 'name': request.form['name'], 'email': request.form['email'],
                             'password': hashedpass})
                return redirect(url_for('login'))
    return render_template('register.html')


# Login Request
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        exist_user = data.find_one({'email': request.form['email']})
        if exist_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), exist_user['password']) == exist_user[
                'password']:
                session['name'] = exist_user['name']
                session['email'] = request.form['email']
                session['logged_in'] = True
                return redirect(url_for('home'))
    return render_template('login.html')


# Basic Content Page
@app.route('/basics', methods=['GET', 'POST'])
def basics():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('basics.html')


# Intermediate Content Page
@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('intermediate.html')


# Advanced Content Page
@app.route('/advanced', methods=['GET', 'POST'])
def advanced():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('advanced.html')


# Logout Request
@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('logged_in', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='localhost', port=8001, debug=True)
