import os

from baseapp import app
from bookiebot import bookiebot


app.register_blueprint(bookiebot)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
