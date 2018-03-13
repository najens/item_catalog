#!/usr/bin/env python
import sys
sys.path.insert(0, 'var/www/catalog')
from app import app as application


if __name__ == '__main__':
    # Run app on localhost port 5000
    application.run()
