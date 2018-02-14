from flask import redirect, url_for, flash, make_response
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import current_user, login_user
from app import app, db
from app.models import User, OAuth
from sqlalchemy.orm.exc import NoResultFound
from datetime import timedelta
from flask_jwt_extended import (
        create_access_token, create_refresh_token,
        set_access_cookies, set_refresh_cookies
)


# Initialize Flask-Dance blueprints
google_blueprint = make_google_blueprint(
    client_id=app.config.get('GOOGLE_ID'),
    client_secret=app.config.get('GOOGLE_SECRET'),
    scope=["profile", "email"],
    redirect_url="/token/google"
)

facebook_blueprint = make_facebook_blueprint(
    client_id=app.config.get('FACEBOOK_APP_ID'),
    client_secret=app.config.get('FACEBOOK_APP_SECRET'),
    scope=["public_profile", "email"],
    redirect_url="/token/facebook"
)

# Setup sqlalchemy backend for blueprints
google_blueprint.backend = SQLAlchemyBackend(
    OAuth,
    db.session,
    user=current_user
)

facebook_blueprint.backend = SQLAlchemyBackend(
    OAuth,
    db.session,
    user=current_user
)


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    """Log in user on successful Google authorization."""
    # If user doesn't have valid oauth token, flash error
    if not token:
        flash("Failed to log in {name}".format(name=blueprint.name))
        return

    # Get user data from oauth session
    resp = blueprint.session.get("/oauth2/v2/userinfo")

    # If failed to get data, flash error
    if not resp.ok:
        msg = "Failed to fetch user info from {name}.".format(
            name=blueprint.name
        )
        flash(msg, category="error")
        return False

    # Setup query
    user_info = resp.json()
    user_id = str(user_info["id"])
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id,
    )

    # Try to find oauth user in database
    try:
        oauth = query.one()

    # If no result found, create new oauth token account for user
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    # If query successful, log in user
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with {name}.".format(
                name=blueprint.name
        ))

    # If query not successful, create new user then log in user
    else:
        # Create a new local user account for this user
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            picture=user_info['picture']
        )
        user.generate_public_id()

        # Associate the new local user account with the OAuth token account
        oauth.user = user

        # Save and commit database models
        db.session.add_all([user, oauth])
        db.session.commit()

        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with {name}.".format(
                name=blueprint.name
        ))

    # Create the tokens to be sent to the user
    expires = timedelta(seconds=20)
    access_token = create_access_token(
        identity=current_user.public_id,
        expires_delta=expires
    )
    refresh_token = create_refresh_token(identity=current_user.public_id)

    # Set JWT cookies in the response and
    # redirect user to the home page
    response = make_response(redirect(url_for('site.index')))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.set_cookie('public_id', current_user.public_id)

    return response


@oauth_error.connect_via(google_blueprint)
def google_error(blueprint, error, error_description=None,
                 error_uri=None):
    """Throw error on authentication failure from Google."""
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")


@oauth_authorized.connect_via(facebook_blueprint)
def facebook_logged_in(blueprint, token):
    """Log in user on successful Facebook authorization."""
    # If user doesn't have valid oauth token, flash error
    if not token:
        flash("Failed to log in {name}".format(name=blueprint.name))
        return

    # Get user data from oauth session
    resp = blueprint.session.get("/me?fields=id,name,email,picture")

    # If failed to get data, flash error
    if not resp.ok:
        msg = "Failed to fetch user info from {name}.".format(
            name=blueprint.name
        )
        flash(msg, category="error")
        return False

    # Setup query
    user_info = resp.json()
    user_id = str(user_info["id"])
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=user_id,
    )

    # Try to find oauth user in database
    try:
        oauth = query.one()

    # If no result found, create new oauth token account for user
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    # If query successful, log in user
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with {name}.".format(
                name=blueprint.name
        ))

    # If query not successful, create new user then log in user
    else:
        # Create a new local user account for this user
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            picture=user_info['picture']['data']['url']
        )
        user.generate_public_id()

        # Associate the new local user account with the OAuth token
        oauth.user = user

        # Save and commit database models
        db.session.add_all([user, oauth])
        db.session.commit()

        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in with {name}.".format(
                name=blueprint.name
        ))

    # Create the tokens to be sent to the user
    expires = timedelta(seconds=8)
    access_token = create_access_token(
        identity=current_user.public_id,
        expires_delta=expires
    )
    refresh_token = create_refresh_token(identity=current_user.public_id)

    # Set JWT cookies in the response and
    # redirect user to the home page
    response = make_response(redirect(url_for('site.index')))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    response.set_cookie('public_id', current_user.public_id)

    return response


@oauth_error.connect_via(facebook_blueprint)
def facebook_error(blueprint, error, error_description=None, error_uri=None):
    """Throw error on authentication failure from Facebook."""
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description} uri={uri}"
    ).format(
        name=blueprint.name,
        error=error,
        description=error_description,
        uri=error_uri,
    )
    flash(msg, category="error")
