from flask import Blueprint


site = Blueprint(
    'site',
    __name__,
    template_folder='./templates',
    static_folder='./static',
    static_url_path='/app/site/static'
)

from .views import catalog, login, tokens  # noqa
