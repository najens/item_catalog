from app import app
from config import db
from flask import render_template, redirect, url_for, request
from models import User, Category, Item
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from user.tokens import is_logged_in

@app.route('/catalog/item/new', methods=['GET', 'POST'])
@jwt_required
def new_item():
    """ Displays page to add a new item to category """
    public_id = get_jwt_identity()
    if request.method == 'POST':

        if (request.form['name'] and request.form['description'] and
                request.form.get('category')):
            new_item = Item(name=request.form['name'],
                    description=request.form['description'],
                    category_name=request.form.get('category'),
                    user_id=public_id)
            db.session.add(new_item)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        logged_in = is_logged_in(public_id)
        categories = Category.query.order_by(db.asc(Category.name)).all()
        return render_template('new_item.html', categories=categories,
                logged_in=logged_in)

@app.route('/catalog/<category>/<int:id>')
@jwt_optional
def item_info(category, id):
    """ Displays page with information about item """
    item = Item.query.filter_by(id=id).one()
    public_id = get_jwt_identity()
    logged_in = is_logged_in(public_id)
    return render_template('item.html', item=item, logged_in=logged_in)

@app.route('/catalog/<category>/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required
def edit_item(category, id):
    """ Displays page to edit item """
    item_to_edit = Item.query.filter_by(id=id).one()
    public_id = get_jwt_identity()

    if item_to_edit.user_id != public_id:
        return 'You are not authorized to edit this category!'

    if request.method == 'POST':
        if (request.form['name'] and request.form['description'] and
                request.form.get('category')):
            item_to_edit.name = request.form['name']
            item_to_edit.description = request.form['description']
            item_to_edit.category_name = request.form.get('category')
            db.session.commit()
            return redirect(url_for('index'))
    else:
        categories = Category.query.order_by(db.asc(Category.name)).all()
        logged_in = is_logged_in(public_id)
        return render_template('edit_item.html', item=item_to_edit,
                categories=categories, logged_in=logged_in)

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
        logged_in = is_logged_in(public_id)
        return render_template('delete_item.html', item=item_to_delete,
                logged_in=logged_in)
