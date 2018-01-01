from flask import Blueprint


bookiebot = Blueprint(
    'bookiebot',
    __name__,
    template_folder='templates'
)

