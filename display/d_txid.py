from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dtxid = Blueprint('display_txid', __name__)

@Dtxid.route("/Dtxid/<string:txid>")
@Dtxid.route("/Dtxid/<string:txid>/")
@Dtxid.route("/Dtxid/<int:dbid>")
@Dtxid.route("/Dtxid/<int:dbid>/")
def display_txid(txid=None, dbid=None):
	
	error_dict = dict()
	
	this_endpoint = g.config_items["self"]["url"] + "/api/txid/" + str(txid)
	#this_endpoint = api_txid(txid=txid, dbid=dbid)
	this_attempts_endpoint = g.config_items["self"]["url"] + "/api/attempts/" + str(txid)
	print(this_endpoint)
		
	# Grab Endpoint
	try: 
		txid_data = requests.get(this_endpoint).content
		txid_attempts = requests.get(this_attempts_endpoint).content
	except Exception as e:
		print(str(e))
	
	stringified = txid_data.decode('utf-8')
	stringified_attempts = txid_attempts.decode('utf-8')
	sanitized = json.loads(stringified)
	sanitized_attempts = json.loads(stringified_attempts)
	
	return render_template('display/Dtxid.html.jinja', data=sanitized, attempts=sanitized_attempts)

