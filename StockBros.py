#!flask/bin/python
from flask import Flask, abort, jsonify, make_response, url_for, request
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import pymongo
from dbWrapper import db
from util import *


#Create application object
app = Flask(__name__)
auth = HTTPBasicAuth()

#####################
#HTTP Authentication#
#####################
@auth.get_password
def get_pw(username):
	documentUsers = db.users
	authUser = documentUsers.find_one({"Username": username})
	if(authUser!=None):
		return authUser.get("pw")
	return None

#########################
#Error control functions#
#########################
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)
	
################
#      GET     #
################
@app.route('/StockBros/events', methods=['GET'])
@auth.login_required
def get_events():
	documentEvents = db.events
	events = []
	
	for event in documentEvents.find({}):
		events.append(event)
	
	return jsonify({'events': [make_public_event(e) for e in events]})

@app.route('/StockBros/events/<int:event_id>', methods=['GET'])
@auth.login_required
def get_event(event_id):
	documentEvents = db.events

	event = documentEvents.find_one({'_id':event_id})
	
	if not event:
		abort(404)

	return jsonify({'event':[make_public_event(event)]})

################
#     POST     #
################
@app.route('/StockBros/events', methods=['POST'])
def create_event():
	if not request.json or not 'title' in request.json:
		abort(400)
	
	documentEvents = db.events
	e = documentEvents.find_one(sort=[("_id", pymongo.DESCENDING)])
	
	event = {
		'_id': e['_id'] + 1,
		'title': request.json['title'],
		'insertDate': str(datetime.now()),
		'eventDate': request.json['eventDate'],
		'text': request.json['text'],
		'href': request.json['href'],
		'stock': request.json['stock'],
		'reaction': request.json['reaction'],
		'variation': request.json['variation']
	}
	
	documentEvents.insert(event)
	return jsonify({'event':[make_public_event(event)]}), 201
	
if __name__ == '__main__':
# for debug --> app.run(debug=True)
	app.run()
