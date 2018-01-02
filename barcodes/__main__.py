import datetime
import glob
import secrets
from hashlib import sha1

from flask import Blueprint, Flask, abort, jsonify, request
from flask.ext.mongoengine import MongoEngine
from flask.ext.redis import FlaskRedis
from flask.ext.security import Security
from flask.ext.wtf import Form
from flask_security import (MongoEngineUserDatastore, RoleMixin, Security,
                            UserMixin, login_required)
from redis.exceptions import RedisError
from wtforms import StringField
from wtforms.validators import InputRequired, Length


MONGO_CFG = ''

db = MongoEngine()


app = Flask('barcodes')
app.config.from_envvar('MONGO_SETTINGS')
app.config.from_envvar('REDIS_SETTINGS')


db.init_app(app)
redis_store = FlaskRedis(app)


hashes = {}
for script in glob.glob('luascripts/*.lua'):
    hash_ = sha1()
    with open(script, 'rb') as f:
        hash_.update(f.read())
        hashes[script] = hash_.hexdigest()


# # # # # # # # # # # # # # # # # # # # # BookieBot API # # # # # # # # # # # # # # # # # #


bookiebot = Blueprint(
    'bookiebot',
    __name__,
    template_folder='templates'
)


@bookiebot.route('/bookiebot/current_checkouts', methods=['GET'])
def current_checkouts():
    pass


@bookiebot.route('/bookiebot/due_by', methods=['GET'])
def what_is_due_by():
    try:
        date_string = request.args['date']
        date_fields = date_string.split('-')
        if len(date_fields) < 2 or len(date_fields) > 3:
            raise ValueError('Must be YYYY-MM-DD or MM-DD.')
    except (KeyError, ValueError):
        return abort(400)

    try:
        if len(date_fields) == 2:
            due_date = datetime.datetime.strptime(
                request.args['date'],
                '%m-%d'
            )
            if due_date.month < datetime.datetime.now().month:
                due_date = due_date.replace(year=due_date.year+1)
        elif len(date_fields) == 3:
            due_date = datetime.datetime.strptime(
                date_string,
                '%Y-%m-%d'
            )
        else:
            raise ValueError('Invalid date')
    except (KeyError, ValueError):
        return abort(400)

    timestamp = int(due_date.timestamp())

    return [

    ]

@bookiebot.route('/bookiebot/make_group', methods=['POST'])
def make_group():
    try:
        name = request.json['name']
        items = request.json['items']
    except KeyError:
        return abort(400)

    id = secrets.token_hex(8)

    try:
        while redis_store.exists(f'group:{id}'):
            id = secrets.token_hex(8)
    except RedisError:
        return abort(500)

    redis_store.hset('group:names', name, id)

    try:
        barcodes = [
            get_barcode(item) for item in items
        ]
    except BarcodeSearchError:
        return abort(400)
    else:
        redis_store.sadd(f'group:{id}:items', *barcodes)

    return jsonify({
        'group_id': id,
    })


@bookiebot.route('/bookiebot/what_has', methods=['GET'])
def what_does_have():
    identifier = request.args['user']
    is_user = redis_store.sismember('names:user', identifier)
    is_production = redis_store.sismember('names:production', identifier)

    if is_user:
        results = []
    elif is_production:
        results = []
    else:
        return abort(400)

    # TODO fix this
    return jsonify({
        'items': results,
    })


@bookiebot.route('/bookiebot/who_produces', methods=['GET'])
def who_produces():
    try:
        production = request.args['production']
    except KeyError:
        abort(400)

    producer = redis_store.get('producers', production)

    return jsonify({
        'production': production,
        'producer': producer,
    })


app.register_blueprint(bookiebot)


# # # # # # # # # # # # # # # # # # # # # Checkouts and Returns # # # # # # # # # # # # # # # # # #

checkout_return = Blueprint('checkout_return', __name__)


@checkout_return.route('/checkout', methods=['GET'])
def check_out():
    return jsonify({

    })


@checkout_return.route('/checkin', methods=['POST'])
def check_in():
    try:
        barcodes = request.json['barcodes']
    except KeyError:
        return abort(400)

    try:
        num_removed = redis_store.zrem('checkouts', *barcodes)
    except RedisError:
        return abort(500)

    if num_removed == len(barcodes):
        return jsonify({

        })
    else:
        return jsonify({

        })


app.register_blueprint(checkout_return)


# # # # # # # # # # # # # # # # # # # # # Search Engine # # # # # # # # # # # # # # # # # #


class BarcodeSearchError(Exception):
    """
    Basic exception for when the search engine
    cannot find anything mathcing
    """


def get_barcode(item: str) -> str:
    return ''


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


user_data_store = MongoEngineUserDatastore(db, user_model=User, role_model=Role)
security = Security(app, user_data_store)


class LoginForm(Form):
    username = StringField(
        'username',
        validators=[InputRequired()]
    )
    cwid = StringField(
        'Campus Wide ID',
        validators=[InputRequired(), Length(min=8, max=8)]
    )


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
