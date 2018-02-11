#!/usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow


# Initialize app
app = Flask(__name__)
app.config.from_object('config')

# Initialize Flask_SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'site.login'

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-Marshmallow
ma = Marshmallow(app)

# Import blueprints
from app.site.views.auth import google_blueprint, facebook_blueprint  # noqa
from app.site import site as site_blueprint  # noqa
from app.api import api as api_blueprint  # noqa

# Register the blueprints
app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")
app.register_blueprint(site_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api/v1")
