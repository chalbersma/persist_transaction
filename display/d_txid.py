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
	
	if txid == None :
		call_var = str(dbid)
	elif dbid == None :
		call_var == str(txid)
	else: 
		# Neither
		raise Exception("Magitian detected: No txid or dbid!")
	
	this_endpoint = g.config_items["self"]["url"] + "/api/txid/" + call_var
	#this_endpoint = api_txid(txid=txid, dbid=dbid)
	this_attempts_endpoint = g.config_items["self"]["url"] + "/api/attempts/" + call_var
			
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

