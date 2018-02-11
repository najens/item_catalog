from flask import render_template, g
from flask_login import login_required
from .login import authenticated
from app.site import site


@site.route('/')
def index():
    """ Displays the home page """
    # Check if user has valid access_token
    logged_in = authenticated()
    user = g.user

    return render_template('index.html', user=user, logged_in=logged_in), 200


@site.route('/category/new')
@login_required
def new_category():
    """ Displays page to add a new category """
    logged_in = authenticated()
    user = g.user

    if logged_in:
        return render_template(
            'new_category.html', user=user, logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/edit')
@login_required
def edit_category(category):
    """ Displays page to edit category """
    # Check if user has an access_token
    logged_in = authenticated()
    user = g.user

    if logged_in:
        category = category.title()

        return render_template(
            'edit_category.html',
            user=user,
            category=category,
            logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/delete')
@login_required
def delete_category(category):
    """ Displays page to delete category """
    # Check if user has an access_token
    logged_in = authenticated()
    user = g.user

    if logged_in:
        category = category.title()

        return render_template(
            'delete_category.html',
            user=user,
            category=category,
            logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    """ Displays page to add a new item to category """
    logged_in = authenticated()
    user = g.user

    if logged_in:
        return render_template(
            'new_item.html', user=user, logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/<int:id>')
def item_info(category, id):
    """ Displays page with information about item """
    logged_in = authenticated()
    user = g.user

    return render_template('item.html', user=user, logged_in=logged_in), 200


@site.route('/<category>/<int:id>/edit')
@login_required
def edit_item(category, id):
    """ Displays page to edit item """
    logged_in = authenticated()
    user = g.user

    if logged_in:
        return render_template(
            'edit_item.html', user=user, logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/<int:id>/delete')
@login_required
def delete_item(category, id):
    """ Displays page to delete item """
    logged_in = authenticated()
    user = g.user

    if logged_in:
        return render_template(
            'delete_item.html', user=user, logged_in=logged_in
        ), 200

    return jsonify({'error': 'Not authorized!'}), 401
