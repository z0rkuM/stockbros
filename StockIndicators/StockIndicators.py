#!flask/bin/python
from flask import Blueprint, jsonify, abort
from Authentication.Authentication import *
from util import *

api_si = Blueprint('api_si', __name__)

@api_si.route("/stock_indicators", methods=['GET'])
@auth.login_required
def get_stock_indicators():
	documentSI = db.stock_indicators
	sis = []
	for stockIndicator in documentSI.find({}):
		sis.append(stockIndicator)
	
	return jsonify({'stock_indicators': [make_public_stock_indicator(si) for si in sis]})
	
@api_si.route('/stock_indicators/<stock_id>', methods=['GET'])
@auth.login_required
def get_event(stock_id):
	documentSI = db.stock_indicators

	si = documentSI.find_one({'stock':stock_id})
	
	if not si:
		abort(404)

	return jsonify({'stock_indicators':[make_public_stock_indicator(si)]})
