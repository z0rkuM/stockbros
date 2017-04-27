#!flask/bin/python
from flask import Flask, abort, jsonify, make_response
from Stocks.Stocks import *
from Events.Events import *
from Authentication.Authentication import *
from datetime import datetime
from dbWrapper import db
from util import *


#Create application object
app = Flask(__name__)
#app.config["DEBUG"] = True
app.register_blueprint(api_stocks, url_prefix="/StockBros")
app.register_blueprint(api_events, url_prefix="/StockBros")

#########################
#Error control functions#
#########################
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)
	
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Bad request'}), 404)

	
if __name__ == '__main__':
	app.run()
