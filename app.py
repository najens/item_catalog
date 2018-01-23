#!/usr/bin/env python
from flask import Flask, render_template, url_for


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

@app.route('/catalog/<category>/new', methods=['GET'], ['POST'])
def new_item(category):
    """ Displays page to add a new item to category """
    return 'Add new item for {} here!'.format(category)

@app.route('/catalog/<category>/<int:id>')
def item_info(category):
    """ Displays page with information about item """
    return 'Display info about {} item #{} here!'.format(category, id)

@app.route('/catalog/<category>/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(category, id):
    """ Displays page to edit item """
    return 'Display page to edit {} item #{} here!'.format(category, id)

@app.route('/catalog/<category>/<int:id>/delete', methods=['GET', 'POST'])
def delete_item(category, id):
    """ Displays page to delete item """
    return 'Display page to delete {} item #{} here!'.format(category, id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
