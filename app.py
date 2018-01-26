#!/usr/bin/env python
from flask import Flask, render_template, url_for, request, redirect, make_response
from models import db, User, Role, UserRoles, Category, Item
from os import path
from flask_httpauth import HTTPBasicAuth
from flask_dance.contrib.google import make_google_blueprint, google


# Initialize app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item_catalog.db'

# Initialize Flask_SQLAlchemy
db.app = app
db.init_app(app)

# Initialize Flask-HTTPAuth
auth = HTTPBasicAuth()

# Initialize Flask-Dance
google_blueprint = make_google_blueprint(
    client_id="117054638326-j19nic44e9a8ountnbfk2jn9ddejmrqc.apps.googleusercontent.com",
    client_secret="LXqfK5z1WuSaZm3ACgh03SAD",
    scope=["email"]
)
app.register_blueprint(google_blueprint, url_prefix="/google_login")

@auth.verify_password
def verify_password(username_or_token, password):
    # try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        return False
    g.user = user
    return True

# Build routes
@app.route('/')
@app.route('/catalog')
def index():
    """ Displays the home page """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.order_by(db.desc(Item.id)).limit(10)
    # Check if user has access_token
    if 'access_token' in request.cookies:
        access_token = request.cookies.get('access_token')
        user = User.verify_auth_token(access_token)
        if user:
            return render_template('index.html', categories=categoires, items=items, user=user)
    else:
        return render_template('public_index.html', categories=categories, items=items)

@app.route('/register')
def register():
    """ Displays the registration page """
    return 'Register here!'

@app.route('/login')
def login():
    """ Displays the login page """
    return render_template('login.html')

@app.route('/oauth/<provider>')
def oauth(provider):
    if provider == google:
        if not google.authorized:
            return redirect(url_for("google.login"))
        account_info = google.get("/oauth2/v2/userinfo")
        if accoun_info.ok:
            account_info_json = account_info.json()
            #see if user exists, if it doesn't make a new one
            user = User.query.filter_by(email=account_info_json['email']).first()
            if not user:
                user = User(provider='google',
                            name=account_info_json['name'],
                            email=account_info_json['email'],
                            picture=account_info_json['picture'])
                user.generate_public_id()
                user.generate_created_at()
                db.session.add(user)
                db.session.commit()
            # generate token
            token = user.generate_auth_token(600)
            response = make_response(redirect(url_for('index')))
            response.set_cookie('access_token', token.decode('ascii'))
            return response
        else:
            return url_for('login')

@app.route('/catalog/category/new', methods=['GET', 'POST'])
@auth.login_required
def new_category():
    """ Displays page to add a new category """
    if request.method == 'POST':
        if request.form['name']:
            new_category = Category(name=request.form['name'], user_id=1)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('new_category.html')

@app.route('/catalog/<category>')
def category(category):
    """ Displays list of items in category """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.filter_by(category_name=category).order_by(db.asc(Item.name)).all()
    return render_template('category.html', items=items, categories=categories, category=category)

@app.route('/catalog/<category>/edit', methods=['GET', 'POST'])
@auth.login_required
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
@auth.login_required
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
@auth.login_required
def new_item():
    """ Displays page to add a new item to category """
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form.get('category'):
            new_item = Item(name=request.form['name'], description=request.form['description'], category_name=request.form.get('category'), user_id=1)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        categories = Category.query.order_by(db.asc(Category.name)).all()
        return render_template('new_item.html', categories=categories)

@app.route('/catalog/<category>/<int:id>')
def item_info(category, id):
    """ Displays page with information about item """
    item = Item.query.filter_by(id=id).one()
    return render_template('item.html', item=item)

@app.route('/catalog/<category>/<int:id>/edit', methods=['GET', 'POST'])
@auth.login_required
def edit_item(category, id):
    """ Displays page to edit item """
    item_to_edit = Item.query.filter_by(id=id).one()
    if item_to_edit.user_id != 1:
        return 'You are not authorized to edit this category!'
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form.get('category'):
            item_to_edit.name = request.form['name']
            item_to_edit.description = request.form['description']
            item_to_edit.category_name = request.form.get('category')
            db.session.commit()
            return redirect(url_for('index'))
    else:
        categories = Category.query.order_by(db.asc(Category.name)).all()
        return render_template('edit_item.html', item=item_to_edit, categories=categories)

@app.route('/catalog/<category>/<int:id>/delete', methods=['GET', 'POST'])
@auth.login_required
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
