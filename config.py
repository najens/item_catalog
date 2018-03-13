# Configure app
DEBUG = True
SECRET_KEY = 'REPLACE THIS WITH SOMETHING SUPER SECRET FOR PRODUCTION'

POSTGRES_USER = 'ubuntu'
POSTGRES_PW = 'mypassword'
POSTGRES_URL = 'lightsaildbinstance.c3holytuhjpo.us-west-2.rds.amazonaws.com'
POSTGRES_PORT = '5432'
POSTGRES_DB = 'catalog'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, port=POSTGRES_PORT,db=POSTGRES_DB)
SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_SECURE = False  # Set to True in production
JWT_ACCESS_COOKIE_PATH = '/api/'
JWT_ACCESS_CSRF_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/token/refresh'
JWT_REFRESH_CSRF_COOKIE_PATH = '/'
JWT_COOKIE_SAMESITE = 'Strict'
JWT_COOKIE_CSRF_PROTECT = True
JWT_SECRET_KEY = 'REPLACE THIS WITH SOMETHING SUPER SECRET FOR PRODUCTION'

# TODO Insert Google Client ID and Secret
GOOGLE_CLIENT_ID = '117054638326-j19nic44e9a8ountnbfk2jn9ddejmrqc.apps.googleusercontent.com'  # noqa
GOOGLE_CLIENT_SECRET = 'LXqfK5z1WuSaZm3ACgh03SAD'

# TODO Insert Facebook App ID and Secret
FACEBOOK_APP_ID = '141117439918918'
FACEBOOK_APP_SECRET = '5f91c11eb7eed46b608dce28a0b6c7ca'

JSON_SORT_KEYS = False
