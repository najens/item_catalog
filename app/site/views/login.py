from app import login_manager
from flask import render_template, g
from app.models import User
from app.site import site
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    """Fetch the associated user from given user_id."""
    return User.query.get(int(user_id))


@site.before_request
def before_request():

    if current_user.is_authenticated:
        g.user = current_user
        g.logged_in = True

    else:
        g.user = "Anonymous"


@site.route('/login')
def login():
    """ Displays the login page """
    return render_template('login.html'), 200


def authenticated():
    """ Check if user is logged in """
    logged_in = False
    if hasattr(g, 'logged_in'):
        if g.logged_in:
            logged_in = True
    return logged_in
