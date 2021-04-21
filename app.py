import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register')
def signup():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/basics')
def basics():
    return render_template('basics.html')

@app.route('/intermediate')
def intermediate():
    return render_template('intermediate.html')

@app.route('/advanced')
def advanced():
    return render_template('advanced.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8001, debug=True)