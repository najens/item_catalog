from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_jwt_extended import JWTManager


# Configure app
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item_catalog.db'
app.config['SECRET_KEY'] = 'supersecret'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/catalog/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

# Initialize Flask_SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Initialize Flask-Dance
google_blueprint = make_google_blueprint(
    client_id="117054638326-j19nic44e9a8ountnbfk2jn9ddejmrqc.apps.googleusercontent.com",
    client_secret="LXqfK5z1WuSaZm3ACgh03SAD",
    scope=["profile", "email"],
    redirect_url="/token/google"
)

facebook_blueprint = make_facebook_blueprint(
    client_id="141117439918918",
    client_secret="5f91c11eb7eed46b608dce28a0b6c7ca",
    scope=["public_profile", "email"],
    redirect_url="/token/facebook"
)

app.register_blueprint(google_blueprint, url_prefix="/google_login")
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")
