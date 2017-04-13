#!flask/bin/python
from flask import url_for

def make_public_event(event):
	recent_event = {}
	for field in event:
		if field == '_id':
			recent_event[field] = event[field]
			recent_event['uri'] = url_for('get_event', event_id=event['_id'], _external=True)
		else:
			recent_event[field] = event[field]
	return recent_event