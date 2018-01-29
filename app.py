#!/usr/bin/env python
from flask import Flask
from os import path


# Initialize app
app = Flask(__name__)

# Import views
from user.login import *
from user.tokens import *
from categories.categories import *
from items.items import *


if __name__ == '__main__':
    if not path.exists('item_catalog.db'):
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
