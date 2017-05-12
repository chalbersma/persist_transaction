from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dwatchtx_results = Blueprint('display_watchtx_results', __name__)

@Dwatchtx_results.route("/Dwatchtx_results/", methods=['GET','POST'])
@Dwatchtx_results.route("/Dwatchtx_results/", methods=['GET','POST'])
def display_watchtx_results(txid=None, email=None):
	
	error = False
	
	if "email" in request.args : 
		email = str(request.args["email"])
	elif "email" in request.form : 
		email = str(request.form["email"])
	
	if "txid" in request.args : 
		txid = str(request.args["txid"])
	elif "txid" in request.form : 
		txid = str(request.form["txid"])
	
	if email != None and txid != None : 
		call_var = "?email=" + str(email) + "&txid=" + str(txid)
	else : 		
		error = True
	
	print(call_var)
	
	if error != True : 	
		this_endpoint = g.config_items["self"]["url"] + "api/watchtx/" + call_var
	
		try: 
			watch_tx_results = requests.get(this_endpoint).content
		except Exception as e:
			print(str(e))
			
		stringified = watch_tx_results.decode('utf-8')
		sanitized = json.loads(stringified)
		if "error" in sanitized.keys() : 
			error = True 
	else :
		sanitized = { "Error" : True }
		error = True
	
	return render_template('display/Dwatchtx_results.html.jinja', error=error, txid=txid, results=sanitized )


