#!/usr/bin/env python
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import sys
sys.path.insert(0, 'var/www/catalog')
from app import app as application


if __name__ == '__main__':
    # Run app on localhost port 5000
    application.run()
