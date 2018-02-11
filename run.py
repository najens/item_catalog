#!/usr/bin/env python
from app import app, db
from os import path

if __name__ == '__main__':
    if not path.exists('item_catalog.db'):
        db.create_all()

    app.run(host='0.0.0.0', port=5000)
