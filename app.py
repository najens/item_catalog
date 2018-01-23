#!/usr/bin/env python
from flask import Flask


# initialize app
app = Flask(__name__)
app.config['DEBUG'] = True

# build routes
@app.route('/')
@app.route('/catalog')
def index():
    return 'Welcome to the item catalog!'

@app.route('/register')
def register():
    return 'Register here!'

@app.route('/login')
def login():
    return 'Login here!'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
