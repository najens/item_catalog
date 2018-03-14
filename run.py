#!/usr/bin/env python
import os
import sys
from app import app as application


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
sys.path.insert(0, 'var/www/catalog')


if __name__ == '__main__':
    # Run app on localhost port 5000
    application.run()
