#!/usr/bin/env python
from flask import Flask


# initialize app
app = Flask(__name__)
app.config['DEBUG'] = True

# build routes
@app.route('/')
def hello():
    return 'Hello World'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
