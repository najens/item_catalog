from app import jwt
from flask import redirect, url_for, make_response, request
from flask_jwt_extended import (
    jwt_required, create_access_token, jwt_refresh_token_required,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies
)
from flask_login import logout_user
from urllib.parse import urlsplit, unquote, urlunsplit
from app.site import site


@jwt.expired_token_loader
def my_expired_token_callback():
    '''This function is called each time a user tries to access a
    jwt_required view with an expired access_token. The user will first be
    sent to the refesh view to get a new access token. They will then be sent
    to the jwt_required view they tried to access
    '''
    request_url = make_safe_url(unquote(request.url))
    return redirect(url_for('site.refresh', next=request_url))


@site.route('/token/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    '''Get the user's id from their refresh_token and create
    a new access token. Send back the access token in the
    response and redirect them to the requested jwt_required view'''
    # Create the new access token
    public_id = get_jwt_identity()
    access_token = create_access_token(identity=public_id)
    # Set the JWT access cookie in the response
    safe_next = _get_safe_next_param('next', 'site.index')
    response = make_response(redirect(safe_next))
    set_access_cookies(response, access_token)
    return response


@site.route('/token/remove', methods=['GET'])
def logout():
    '''Sends a response to the user to delete access and refresh
    tokens and then returns them to the home page'''
    logout_user()
    response = make_response(redirect(url_for('site.index')))
    response.delete_cookie('public_id')
    unset_jwt_cookies(response)
    return response


def make_safe_url(url):
    '''Turns an unsafe absolute URL into a safe
    relative URL by removing the scheme and hostname'''
    parts = urlsplit(url)
    safe_url = urlunsplit(('', '', parts.path, parts.query, parts.fragment))
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
    url = url_for('site.index')
    if endpoint:
        url = url_for(endpoint)
    return url
