from flask import Blueprint, abort, jsonify, request
from redis.exceptions import RedisError

from baseapp import redis_store


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
