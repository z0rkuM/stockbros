#!flask/bin/python
from flask import Blueprint, jsonify

api_si = Blueprint('api_si', __name__)

@api_si.route("/stock_indicators")
def get_stock_indicators():
    return jsonify(stock_indicators=[
        {"username": "alice", "user_id": 1},
        {"username": "bob", "user_id": 2}
    ])
