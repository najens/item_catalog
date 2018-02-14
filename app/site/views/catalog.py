from flask import render_template, g
from flask_login import login_required
from .login import authenticated
from app.site import site


@site.route('/')
def index():
    """
    Displays the home page.
    This is a public non-protected endpoint.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    return render_template('index.html', user=user, logged_in=logged_in), 200


@site.route('/category/new')
@login_required
def new_category():
    """
    Displays page to add a new category.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        return render_template(
            'new_category.html', user=user, logged_in=logged_in
        ), 200

    # If user not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/edit')
@login_required
def edit_category(category):
    """
    Displays page to edit category.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        category = category.title()

        return render_template(
            'edit_category.html',
            user=user,
            category=category,
            logged_in=logged_in
        ), 200

    # If user not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/delete')
@login_required
def delete_category(category):
    """
    Displays page to delete category.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        category = category.title()

        return render_template(
            'delete_category.html',
            user=user,
            category=category,
            logged_in=logged_in
        ), 200

    # If user not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    """
    Displays page to add a new item to category.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        return render_template(
            'new_item.html', user=user, logged_in=logged_in
        ), 200

    # If user not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/<int:id>')
def item_info(category, id):
    """
    Displays page with information about item.
    This is a public non-protected endpoint.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    return render_template('item.html', user=user, logged_in=logged_in), 200


@site.route('/<category>/<int:id>/edit')
@login_required
def edit_item(category, id):
    """
    Displays page to edit item.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        return render_template(
            'edit_item.html', user=user, logged_in=logged_in
        ), 200

    # If user is not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401


@site.route('/<category>/<int:id>/delete')
@login_required
def delete_item(category, id):
    """
    Displays page to delete item.
    This is a protected endpoint and requires valid session cookie.
    """
    # Check if user is logged in
    logged_in = authenticated()
    user = g.user

    # If user is logged in, display page
    if logged_in:
        return render_template(
            'delete_item.html', user=user, logged_in=logged_in
        ), 200

    # If user is not logged in, return error
    return jsonify({'error': 'Not authorized!'}), 401
