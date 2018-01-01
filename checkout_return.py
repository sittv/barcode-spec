from flask import abort, jsonify, request
from redis.exceptions import RedisError

from baseapp import app, redis_store


@app.route('/checkin', methods=['POST'])
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
