from flask import Blueprint


# Setup site blueprint
site = Blueprint(
    'site',
    __name__,
    template_folder='./templates',
    static_folder='./static',
    static_url_path='/app/site/static'
)

# Import blueprint views
from .views import catalog, login, tokens  # noqa
