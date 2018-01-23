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

@app.route('/catalog/category/new', methods=['GET', 'POST'])
def new_category():
    """ Displays page to add a new category """
    return 'Add new category here!'

@app.route('/catalog/<category>')
def category(category):
    """ Displays list of items in category """
    return 'Show list of items for {}!'.format(category)

@app.route('/catalogy/<category>/edit', methods=['GET', 'POST'])
def edit_category(category):
    """ Displays page to edit category """
    return 'Edit {} here!'.format(category)

@app.route('/catalogy/<category>/delete', methods=['GET', 'POST'])
def edit_category(category):
    """ Displays page to delete category """
    return 'Delete {} here!'.format(category)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
