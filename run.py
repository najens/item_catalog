#!/usr/bin/env python
from app import app


if __name__ == '__main__':
    # Run app on localhost port 5000
    app.run(host='0.0.0.0', port=5000)
