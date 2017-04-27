#!flask/bin/python
from flask import Blueprint, jsonify, abort, request
from Authentication.Authentication import *
from datetime import datetime
import pymongo
from util import *

api_events = Blueprint('api_events', __name__)

@api_events.route('/events', methods=['GET'])
@auth.login_required
def get_events():
	documentEvents = db.events
	events = []
	
	for event in documentEvents.find({}):
		events.append(event)
	
	return jsonify({'events': [make_public_event(e) for e in events]})

@api_events.route('/events/<int:event_id>', methods=['GET'])
@auth.login_required
def get_event(event_id):
	documentEvents = db.events

	event = documentEvents.find_one({'_id':event_id})
	
	if not event:
		abort(404)

	return jsonify({'event':[make_public_event(event)]})

@api_events.route('/events', methods=['POST'])
@auth.login_required
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
