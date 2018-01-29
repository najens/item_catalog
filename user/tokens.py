from app import app
from config import jwt, db
from flask import render_template, redirect, url_for, make_response, request
from models import User
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook
from flask_jwt_extended import (jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies)
from datetime import timedelta
from urllib.parse import urlsplit, unquote


@jwt.expired_token_loader
def my_expired_token_callback():
    '''This function is called each time a user tries to access a
    jwt_required view with an expired access_token. The user will first be
    sent to the refesh view to get a new access token. They will then be sent
    to the jwt_required view they tried to access
    '''
    request_url = request.path
    app.logger.info(request_url)
    return redirect(url_for('refresh', next=request_url))

@app.route('/token/<provider>', methods=['GET'])
def get_auth_token(provider):
    '''Checks if user is authorized by provider. If not, send them
    to the provider's log in page, otherwise get their account info from the
    provider's api. If the user doesn't exist, make a new one. Then create
    JWT access and refresh tokens that will be sent back to the user
    '''
    if provider not in ('facebook', 'google'):
        return redirect(url_for('login'))

    if provider == 'google':
        if not google.authorized:
            return redirect(url_for("google.login"))
        account_info = google.get("/oauth2/v2/userinfo")
        if account_info.ok:
            account_info_json = account_info.json()
            # See if user exists, if it doesn't make a new one
            user = User.query.filter_by(
                    email=account_info_json['email']).first()
            if not user:
                user = User(provider='google',
                            name=account_info_json['name'],
                            email=account_info_json['email'],
                            picture=account_info_json['picture'])
                user.generate_public_id()
                user.generate_created_at()
                db.session.add(user)
                db.session.commit()
        else:
            return "Something went wrong"

    if provider == 'facebook':
        if not facebook.authorized:
            return redirect(url_for("facebook.login"))
        account_info = facebook.get("/me?fields=id,name,email,picture")
        if account_info.ok:
            account_info_json = account_info.json()
            # See if user exists, if it doesn't make a new one
            user = User.query.filter_by(
                    email=account_info_json['email']).first()
            if not user:
                user = User(provider='facebook',
                        name=account_info_json['name'],
                        email=account_info_json['email'],
                        picture=account_info_json['picture']['data']['url'])
                user.generate_public_id()
                user.generate_created_at()
                db.session.add(user)
                db.session.commit()
        else:
            return "Something went wrong"

    # Create the tokens we will be sending back to the user
    expires = timedelta(seconds=20)
    access_token = create_access_token(identity=user.public_id,
            expires_delta=expires)
    refresh_token = create_refresh_token(identity=user.public_id)

    # Set the JWT cookies in the response
    response = make_response(redirect(url_for('index')))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response

@app.route('/token/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    '''Get the user's id from their refresh_token and create
    a new access token. Send back the access token in the
    response and redirect them to the requested jwt_required view'''
    # Create the new access token
    public_id = get_jwt_identity()
    access_token = create_access_token(identity=public_id)

    # Set the JWT access cookie in the response
    safe_next = _get_safe_next_param('next', 'index')
    response = make_response(redirect(safe_next))
    set_access_cookies(response, access_token)
    return response

@app.route('/catalog/token/remove', methods=['GET'])
@jwt_required
def logout():
    '''Sends a response to the user to delete access and refresh
    tokens and then returns them to the home page'''
    response = make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response

def make_safe_url(url):
    '''Turns an unsafe absolute URL into a safe
    relative URL by removing the scheme and hostname'''
    parts = urlsplit(url)
    safe_url = parts.path+parts.query+parts.fragment
    return safe_url

def _get_safe_next_param(param_name, default_endpoint):
    '''The next query parameter contains quoted URLs that may contain
    unsafe hostnames. Return the query parameter as a safe, unquoted URL'''
    if param_name in request.args:
        # Return safe unquoted query parameter value
        safe_next = make_safe_url(unquote(request.args[param_name]))
    else:
        # Return URL of default endpoint
        safe_next = _endpoint_url(default_endpoint)
    return safe_next

def _endpoint_url(endpoint):
    '''If default endpoint is not specified, return to home page'''
    url = url_for('index')
    if endpoint:
        url = url_for(endpoint)
    return url

def is_logged_in(public_id):
    '''Check if user is logged in'''
    if public_id != None:
        return True
    else:
        return False
