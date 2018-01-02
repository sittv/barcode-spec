import json

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.redis import FlaskRedis

MONGO_CFG = ''

db = MongoEngine()


app = Flask('barcodes')

with open(MONGO_CFG) as f:
    app.config['MONGODB_SETTINGS'] = json.load(f)

db.init_app(app)


redis_store = FlaskRedis(app)