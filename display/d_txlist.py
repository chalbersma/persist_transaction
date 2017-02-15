from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dtxlist = Blueprint('display_txlist', __name__)

@Dtxlist.route("/Dtxlist", methods=['GET'])
@Dtxlist.route("/Dtxlist/", methods=['GET'])
def display_txlist(inactive=None, amount=None):
	
	error_dict = dict()
	
	query_list = list()
	
	inactive = request.args.get("inactive", default=None)
	amount = request.args.get("amount", default=None)
	
	print(amount)
	print(type(amount))
	
	if inactive != None :
		query_list.append("inactive=true")
	
	if amount != None :
		query_list.append("amount="+str(amount))
		
	this_endpoint = g.config_items["self"]["url"] + "api/txlist/?" + "&".join(query_list)
		
	try: 
		txlist_data = requests.get(this_endpoint).content
	except Exception as e:
		print(str(e))
	
	stringified = txlist_data.decode('utf-8')
	sanitized = json.loads(stringified)
	
	if "error" in sanitized.keys() :
		txlistdata = False 
	else :
		txlistdata = True
		
	success_fail = { "txlist" : txlistdata }
	
	return render_template('display/Dtxlist.html.jinja', txlist=sanitized, gotdata=success_fail)

