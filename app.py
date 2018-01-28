#!/usr/bin/env python
from flask import Flask, render_template, url_for, request, redirect, make_response
from models import db, User, Role, UserRoles, Category, Item
from os import path
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import logging
from logging.handlers import RotatingFileHandler
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, jwt_optional
)
from datetime import timedelta
from urllib.parse import urlsplit, unquote


# Initialize app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item_catalog.db'
app.config['SECRET_KEY'] = 'supersecret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/catalog/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize Flask_SQLAlchemy
db.app = app
db.init_app(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-Dance
google_blueprint = make_google_blueprint(
    client_id="117054638326-j19nic44e9a8ountnbfk2jn9ddejmrqc.apps.googleusercontent.com",
    client_secret="LXqfK5z1WuSaZm3ACgh03SAD",
    scope=["profile", "email"],
    redirect_url="/token/google"
)

facebook_blueprint = make_facebook_blueprint(
    client_id="141117439918918",
    client_secret="5f91c11eb7eed46b608dce28a0b6c7ca",
    scope=["public_profile", "email"],
    redirect_url="/token/facebook"
)

app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")

@jwt.expired_token_loader
def my_expired_token_callback():
    request_url = request.path
    app.logger.info(request_url)
    return redirect(url_for('refresh', next=request_url))

# Build routes
@app.route('/catalog/')
@jwt_optional
def index():
    """ Displays the home page """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.order_by(db.desc(Item.id)).limit(10)
    # Check if user has valid access_token
    public_id = get_jwt_identity()
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        return render_template('index.html', categories=categories, items=items, user=user)
    else:
        return render_template('public_index.html', categories=categories, items=items)

@app.route('/login')
def login():
    """ Displays the login page """
    return render_template('login.html')

@app.route('/oauth/<provider>')
def oauth(provider):
    app.logger.info(provider)
    if provider == 'google':
        app.logger.info(google.authorized)
        if not google.authorized:
            return redirect(url_for("google.login"))
        else:
            return redirect(url_for("get_auth_token", provider=provider))
    elif provider == 'facebook':
        if not facebook.authorized:
            return redirect(url_for("facebook.login"))
        else:
            return redirect(url_for("get_auth_token", provider=provider))
    else:
        return redirect(url_for('login'))

@app.route('/token/<provider>', methods=['GET'])
def get_auth_token(provider):

    if provider == 'google':
        if not google.authorized:
            return redirect(url_for("google.login"))
        account_info = google.get("/oauth2/v2/userinfo")
        if account_info.ok:
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
            # Create the tokens we will be sending back to the user
            expires = timedelta(seconds=20)
            access_token = create_access_token(identity=user.public_id, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user.public_id)

            # Set the JWT cookies in the response
            response = make_response(redirect(url_for('index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

    if provider == 'facebook':
        if not facebook.authorized:
            return redirect(url_for("facebook.login"))
        account_info = facebook.get("/me?fields=id,name,email,picture")
        if account_info.ok:
            account_info_json = account_info.json()
            # see if user exists, if it doesn't make a new one
            user = User.query.filter_by(email=account_info_json['email']).first()
            if not user:
                user = User(provider='facebook',
                            name=account_info_json['name'],
                            email=account_info_json['email'],
                            picture=account_info_json['picture']['data']['url'])
                user.generate_public_id()
                user.generate_created_at()
                db.session.add(user)
                db.session.commit()

            # Create the tokens we will be sending back to the user
            expires = timedelta(seconds=20)
            access_token = create_access_token(identity=user.public_id, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user.public_id)

            # Set the JWT cookies in the response
            response = make_response(redirect(url_for('index')))
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response

    if provider != 'facebook' or 'google':
        return redirect(url_for('login'))



@app.route('/token/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the JWT access cookie in the response
    safe_next = _get_safe_next_param('next', 'index')
    response = make_response(redirect(safe_next))
    set_access_cookies(response, access_token)
    return response

@app.route('/catalog/token/remove', methods=['GET'])
@jwt_required
def logout():
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response

@app.route('/catalog/category/new', methods=['GET', 'POST'])
@jwt_required
def new_category():
    """ Displays page to add a new category """
    if request.method == 'POST':
        if request.form['name']:
            public_id = get_jwt_identity()
            new_category = Category(name=request.form['name'], user_id=public_id)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('new_category.html')

@app.route('/catalog/<category>')
@jwt_optional
def category(category):
    """ Displays list of items in category """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.filter_by(category_name=category).order_by(db.asc(Item.name)).all()
    # Check if user has valid access_token
    public_id = get_jwt_identity()
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        return render_template('category.html', items=items, categories=categories, category=category, user=user)
    else:
        return render_template('public_category.html', items=items, categories=categories, category=category)

@app.route('/catalog/<category>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_category(category):
    """ Displays page to edit category """
    category_to_edit = Category.query.filter_by(name=category).one()
    public_id = get_jwt_identity()
    if category_to_edit.user_id != public_id:
        return 'You are not authorized to edit this category!'
    if request.method == 'POST':
        if request.form['name']:
            category_to_edit.name = request.form['name']
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('edit_category.html', category=category_to_edit)

@app.route('/catalog/<category>/delete', methods=['GET', 'POST'])
@jwt_required
def delete_category(category):
    """ Displays page to delete category """
    category_to_delete = Category.query.filter_by(name=category).one()
    public_id = get_jwt_identity()
    if category_to_delete.user_id != public_id:
        return "You are not authorized to delete this category!"
    if request.method == 'POST':
        db.session.delete(category_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('delete_category.html', category=category_to_delete)

@app.route('/catalog/item/new', methods=['GET', 'POST'])
@jwt_required
def new_item():
    """ Displays page to add a new item to category """
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and request.form.get('category'):
            public_id = get_jwt_identity()
            new_item = Item(name=request.form['name'], description=request.form['description'], category_name=request.form.get('category'), user_id=public_id)
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
@jwt_required
def edit_item(category, id):
    """ Displays page to edit item """
    item_to_edit = Item.query.filter_by(id=id).one()
    public_id = get_jwt_identity()
    if item_to_edit.user_id != public_id:
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
@jwt_required
def delete_item(category, id):
    """ Displays page to delete item """
    item_to_delete = Item.query.filter_by(id=id).one()
    public_id = get_jwt_identity()
    if item_to_delete.user_id != public_id:
        return "You are not authorized to delete this category!"
    if request.method == 'POST':
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('delete_item.html', item=item_to_delete)

# Turns an usafe absolute URL into a safe relative URL by removing the scheme and the hostname
# Example: make_safe_url('http://hostname/path1/path2?q1=v1&q2=v2#fragment')
#          returns: '/path1/path2?q1=v1&q2=v2#fragment
def make_safe_url(url):
    parts = urlsplit(url)
    safe_url = parts.path+parts.query+parts.fragment
    return safe_url


# 'next' and 'reg_next' query parameters contain quoted (URL-encoded) URLs
# that may contain unsafe hostnames.
# Return the query parameter as a safe, unquoted URL
def _get_safe_next_param(param_name, default_endpoint):
    if param_name in request.args:
        # return safe unquoted query parameter value
        safe_next = make_safe_url(unquote(request.args[param_name]))
    else:
        # return URL of default endpoint
        safe_next = _endpoint_url(default_endpoint)
    return safe_next


def _endpoint_url(endpoint):
    url = '/catalog/'
    if endpoint:
        url = url_for(endpoint)
    return url


if __name__ == '__main__':
    if not path.exists('item_catalog.db'):
        db.create_all()
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} - %(name)s - %(levelname)s - %(message)s")
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000)
