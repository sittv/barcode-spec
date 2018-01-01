import os

from flask import Flask
from bookiebot import bookiebot


app = Flask(__name__)
app.register_blueprint(bookiebot)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
