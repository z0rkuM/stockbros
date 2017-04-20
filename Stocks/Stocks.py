#!flask/bin/python
from flask import Blueprint, jsonify, abort
from Authentication.Authentication import *
from util import *

api_stocks = Blueprint('api_stocks', __name__)

@api_stocks.route("/stocks", methods=['GET'])
@auth.login_required
def get_stocks():
	documentStocks = db.stocks
	stocks = []
	for stock in documentStocks.find({}):
		stocks.append(stock)
	return jsonify({'stocks': [make_public_stock(s) for s in stocks]})
	
@api_stocks.route('/stocks/<stock_id>', methods=['GET'])
@auth.login_required
def get_stock(stock_id):
	documentStocks = db.stocks

	stock = documentStocks.find_one({'stock':stock_id})
	
	if not stock:
		abort(404)

	return jsonify({'stocks':[make_public_stock(stock)]})
