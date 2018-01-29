from app import app
from config import db
from flask import render_template, redirect, url_for, request
from models import User, Category, Item
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from user.tokens import is_logged_in


@app.route('/catalog/')
@jwt_optional
def index():
    """ Displays the home page """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.order_by(db.desc(Item.id)).limit(10)
    # Check if user has valid access_token
    public_id = get_jwt_identity()
    logged_in = is_logged_in(public_id)
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        return render_template('index.html', categories=categories,
                items=items, user=user, logged_in=logged_in)
    else:
        return render_template('public_index.html', categories=categories,
                items=items, logged_in=logged_in)

@app.route('/catalog/category/new', methods=['GET', 'POST'])
@jwt_required
def new_category():
    """ Displays page to add a new category """
    public_id = get_jwt_identity()
    if request.method == 'POST':
        if request.form['name']:
            new_category = Category(name=request.form['name'],
                    user_id=public_id)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        logged_in = is_logged_in(public_id)
        return render_template('new_category.html', logged_in=logged_in)

@app.route('/catalog/<category>')
@jwt_optional
def category(category):
    """ Displays list of items in category """
    categories = Category.query.order_by(db.asc(Category.name)).all()
    items = Item.query.filter_by(
            category_name=category).order_by(db.asc(Item.name)).all()
    # Check if user has valid access_token
    public_id = get_jwt_identity()
    logged_in = is_logged_in(public_id)
    user = User.query.filter_by(public_id=public_id).first()
    if user:
        return render_template('category.html', items=items,
                categories=categories, category=category,
                logged_in=logged_in, user=user)
    else:
        return render_template('public_category.html', items=items,
                categories=categories, category=category, logged_in=logged_in)

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
        logged_in = is_logged_in(public_id)
        return render_template('edit_category.html',
                category=category_to_edit, logged_in=logged_in)

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
        logged_in = is_logged_in(public_id)
        return render_template('delete_category.html',
                category=category_to_delete, logged_in=logged_in)
