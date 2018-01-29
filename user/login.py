from app import app
from flask import render_template, redirect, url_for
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook


@app.route('/login')
def login():
    """ Displays the login page """
    return render_template('login.html')

@app.route('/oauth/<provider>')
def oauth(provider):
    if provider == 'google':
        if not google.authorized:
            return redirect(url_for('google.login'))
        else:
            return redirect(url_for('get_auth_token', provider=provider))
    elif provider == 'facebook':
        if not facebook.authorized:
            return redirect(url_for('facebook.login'))
        else:
            return redirect(url_for('get_auth_token', provider=provider))
    else:
        return redirect(url_for('login'))
