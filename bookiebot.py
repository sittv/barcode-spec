from functools import partial
import secrets

from flask import Blueprint, abort, jsonify, request

from baseapp import app, redis_store


class BarcodeSearchError(Exception):
    """
    Exception raised when no matching barcode
    can be found.
    """


bookiebot = Blueprint(
    'bookiebot',
    __name__,
    template_folder='templates'
)


@bookiebot.route('/current_checkouts', methods=['GET'])
def current_checkouts():
    pass


@bookiebot.route('/make_group', methods=['POST'])
def make_group():
    try:
        name = request.json['name']
        items = request.json['items']
    except KeyError:
        abort(400)

    for id in iter(partial(secrets.token_hex, 8)):
        try:
            if not redis_store.exists(f'group:{id}'):
                break
        except:
            pass
        
    try:
        barcodes = [
            _get_barcode(item) for item in items
        ]
    except BarcodeSearchError:
        abort(400)

    return jsonify({
        'group_id': id,
    })
