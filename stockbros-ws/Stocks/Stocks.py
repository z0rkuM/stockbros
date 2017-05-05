#!flask/bin/python
from flask import Blueprint, jsonify, abort, request, make_response
from Authentication.Authentication import *
from util import *

api_stocks = Blueprint('api_stocks', __name__)

@api_stocks.route("/stocks", methods=['GET'])
@auth.login_required
def get_stocks():
	documentStocks = db.stocks
	stocks = []
	for stock in documentStocks.find({}):
		stock.pop("_id")
		stocks.append(stock)
	return jsonify({'stocks': [make_public_stock(s) for s in stocks]})
	
@api_stocks.route('/stocks/<stock_id>', methods=['GET'])
@auth.login_required
def get_stock(stock_id):
	documentStocks = db.stocks

	stock = documentStocks.find_one({'stock':stock_id})
	
	if not stock:
		abort(404)
	
	stock.pop("_id")

	return jsonify({'stocks':[make_public_stock(stock)]})

@api_stocks.route('/stocks', methods=['PUT'])
@auth.login_required
def create_or_update_stock():

	if not request.json:
		abort(400)
		
	stocksSize = len(request.json)
	
	documentStocks = db.stocks
	#matchedCount = 0
	#modifiedCount = 0
	for stock in request.json:
		#result = documentStocks.replace_one({"$and":[{"market": {'$eq':stock['market']}},{"stock": {'$eq':stock['stock']}}]}, stock, True)
		#matchedCount = matchedCount + result.matched_count
		#modifiedCount = modifiedCount + result.modified_count
		result = documentStocks.find_and_modify(query={"$and":[{"market": stock['market']},{"stock": stock['stock']}]}, update=stock, new=True, upsert=True)
	
	#return make_response(jsonify({'stocks':[{ "stocks_inserted" : stocksSize - modifiedCount},{ "stocks_modified" : modifiedCount}]}), 200)
	return make_response(jsonify({'stocks':[{ "result" : "ok"}]}), 200)
