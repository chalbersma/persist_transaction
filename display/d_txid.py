from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dtxid = Blueprint('display_txid', __name__)

@Dtxid.route("/Dtxid/<txid>")
@Dtxid.route("/Dtxid/<txid>/")
def display_txid(txid=None, dbid=None):
	
	error_dict = dict()
		
	this_endpoint = "http://127.0.0.1:8080" + "/api/txid/" + str(txid)
	print(this_endpoint)
		
	# Grab Endpoint
	try: 
		txid_data = requests.get(this_endpoint).content
	except Exception as e:
		print(str(e))
	
	stringified = txid_data.decode('utf-8')
	sanitized = json.loads(stringified)

	return jsonify(sanitized)
		
	#print(hosts_list)
	
	#return render_template('display/Dtxid.html.jinja', hosts_list=hosts_list)

