# Configure app
DEBUG = True
SECRET_KEY = 'supersecret'

SQLALCHEMY_DATABASE_URI = 'sqlite:///item_catalog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_SECURE = False  # Set to True in production
JWT_ACCESS_COOKIE_PATH = '/api/'
JWT_ACCESS_CSRF_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/token/refresh'
JWT_REFRESH_CSRF_COOKIE_PATH = '/'
JWT_COOKIE_SAMESITE = 'Strict'
JWT_COOKIE_CSRF_PROTECT = True
JWT_SECRET_KEY = 'super-secret'

GOOGLE_ID = '117054638326-j19nic44e9a8ountnbfk2jn9ddejmrqc.apps.googleusercontent.com'  # noqa
GOOGLE_SECRET = "LXqfK5z1WuSaZm3ACgh03SAD"

FACEBOOK_APP_ID = '141117439918918'
FACEBOOK_APP_SECRET = '5f91c11eb7eed46b608dce28a0b6c7ca'

JSON_SORT_KEYS = False
