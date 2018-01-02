from flask import Flask
from flask.ext.redis import FlaskRedis


app = Flask('barcodes')

redis_store = FlaskRedis(app)