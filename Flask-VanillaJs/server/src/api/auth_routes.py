"""
This is where we will
"""

from flask import (
    Blueprint,
    jsonify
)

auth_bp = Blueprint(
    'auth',
    __name__,
)

@auth_bp.route('/', methods=['GET'])
def sample_route():
    return jsonify({"message": "this is a non-versioned sample api"})
