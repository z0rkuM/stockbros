#!flask/bin/python
from flask import url_for

def make_public_event(event):
	event['uri'] = url_for('.get_event', event_id=event['_id'], _external=True)
	return event
	
def make_public_stock(stock):
	stock['uri'] = url_for('.get_stock', stock_id=stock['stock'], _external=True)
	return stock
