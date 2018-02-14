#!/usr/bin/env python
from app import app, db
from os import path

if __name__ == '__main__':
    # Create item_catalog database if it doesn't exist
    if not path.exists('item_catalog.db'):
        db.create_all()
    # Run app on localhost port 5000
    app.run(host='0.0.0.0', port=5000)
