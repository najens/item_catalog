#!/usr/bin/env python
from flask import Flask


# initialize app
app = Flask(__name__)
app.config['DEBUG'] = True

# build routes
@app.route('/')
@app.route('/catalog')
def index():
    """ Displays the home page """
    return 'Welcome to the item catalog!'

@app.route('/register')
def register():
    """ Displays the registration page """
    return 'Register here!'

@app.route('/login')
def login():
    """ Displays the login page """
    return 'Login here!'

@app.route('/catalog/category/new')
def new_category():
    """ Displays page to add a new category """
    return 'Add new category here!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
