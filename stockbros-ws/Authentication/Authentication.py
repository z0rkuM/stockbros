#!flask/bin/python
from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from dbWrapper import db

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
	documentUsers = db.users
	authUser = documentUsers.find_one({"Username": username})
	if(authUser!=None):
		return authUser.get("pw")
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def authenticate(username, password):
	documentUsers = db.users
	authUser = documentUsers.find_one({"Username": username, "pw": password})
	if(authUser!=None):
		return authUser
	return None