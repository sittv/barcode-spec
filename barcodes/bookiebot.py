import datetime
import glob
from hashlib import sha1
import secrets

from flask import Blueprint, abort, jsonify, request
from redis import RedisError

from barcodes.baseapp import redis_store
from barcodes.search import get_barcode


class BarcodeSearchError(Exception):
    """
    Exception raised when no matching barcode
    can be found.
    """


hashes = {}
for script in glob.glob('luascripts/*.lua'):
    hash_ = sha1()
    with open(script, 'rb') as f:
        hash_.update(f.read())
        hashes[script] = hash_.hexdigest()


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
