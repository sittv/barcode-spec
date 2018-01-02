from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.redis import FlaskRedis
from flask.ext.security import Security

MONGO_CFG = ''

db = MongoEngine()


app = Flask('barcodes')
app.config.from_envvar('MONGO_SETTINGS')
app.config.from_envvar('REDIS_SETTINGS')


db.init_app(app)
redis_store = FlaskRedis(app)
