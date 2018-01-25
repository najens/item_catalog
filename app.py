#!/usr/bin/env python
from flask import Flask, render_template, url_for, request, redirect
from models import db, User, Role, UserRoles, Category, Item
from os import path


# Initialize app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item_catalog.db'

# Initialize Flask_SQLAlchemy
db.app = app
db.init_app(app)

# Build routes
@app.route('/')
@app.route('/catalog')
def index():
    """ Displays the home page """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.order_by(db.desc(Item.id)).limit(10)
    return render_template('index.html', categories=categories, items=items)

@app.route('/register')
def register():
    """ Displays the registration page """
    return 'Register here!'

@app.route('/login')
def login():
    """ Displays the login page """
    return render_template('login.html')

@app.route('/catalog/category/new', methods=['GET', 'POST'])
def new_category():
    """ Displays page to add a new category """
    if request.method == 'POST':
        new_category = Category(name=request.form['name'], user_id=1)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('new_category.html')

@app.route('/catalog/<category>')
def category(category):
    """ Displays list of items in category """
    return 'Show list of items for {}!'.format(category)

@app.route('/catalogy/<category>/edit', methods=['GET', 'POST'])
def edit_category(category):
    """ Displays page to edit category """
    category_to_edit = Category.query.filter_by(name=category).one()
    if category_to_edit.user_id != 1:
        return 'You are not authorized to edit this category!'
    if request.method == 'POST':
        if request.form['name']:
            category_to_edit.name = request.form['name']
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('edit_category.html', category=category_to_edit)

@app.route('/catalog/<category>/delete', methods=['GET', 'POST'])
def delete_category(category):
    """ Displays page to delete category """
    category_to_delete = Category.query.filter_by(name=category).one()
    if category_to_delete.user_id != 1:
        return "You are not authorized to delete this category!"
    if request.method == 'POST':
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('delete_category.html', category=category_to_delete)

@app.route('/catalog/item/new', methods=['GET', 'POST'])
def new_item():
    """ Displays page to add a new item to category """
    if request.method == 'POST':
        category = request.form.get('category')
        category = Category.query.filter_by(name=category).one()
        new_item = Item(name=request.form['name'], description=request.form['description'], category_id=category.id, user_id=1)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        categories = Category.query.all()
        return render_template('new_item.html', categories=categories)

@app.route('/catalog/<category>/<int:id>')
def item_info(category):
    """ Displays page with information about item """
    return 'Display info about {} item #{} here!'.format(category, id)

@app.route('/catalog/<category>/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(category, id):
    """ Displays page to edit item """
    item_to_edit = Item.query.filter_by(id=id).one()
    if item_to_edit.user_id != 1:
        return 'You are not authorized to edit this category!'
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form.get('category'):
            category = request.form.get('category')
            category = Category.query.filter_by(name=category).one()
            item_to_edit.name = request.form['name']
            item_to_edit.description = request.form['description']
            item_to_edit.category_id = category.id
            db.session.commit()
            return redirect(url_for('index'))
    else:
        categories = Category.query.order_by(db.asc(Category.name)).all()
        return render_template('edit_item.html', item=item_to_edit, categories=categories)

@app.route('/catalog/<category>/<int:id>/delete', methods=['GET', 'POST'])
def delete_item(category, id):
    """ Displays page to delete item """
    item_to_delete = Item.query.filter_by(id=id).one()
    if item_to_delete.user_id != 1:
        return "You are not authorized to delete this category!"
    if request.method == 'POST':
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('delete_item.html', item=item_to_delete)


if __name__ == '__main__':
    if not path.exists('item_catalog.db'):
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
