from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests

# Results of Attempting to Add Transaction.

Dremovetx_results = Blueprint('display_removetx_results', __name__)

@Dremovetx_results.route("/Dremovetx_results/", methods=['GET', 'POST'])
@Dremovetx_results.route("/Dremovetx_results/", methods=['GET', 'POST'])
def display_removetx_results(txid=None, confirmstring=None):
	
	error = False
	
	if "txid" in request.args : 
		txid = str(request.args["txid"])
	
	if "txid" in request.form : 
		txid = str(request.form["txid"])
	
	if "confirmstring" in request.form : 
		confirmstring = str(request.form["confirmstring"])
	
	if txid == None : 
		error = True
	
	if confirmstring == None : 
		error = True
	
	if error != True : 	
		query_string = "?txid=" + txid + "&confirmstring=" + confirmstring
		this_endpoint = g.config_items["self"]["url"] + "api/removetx/" + query_string
	
		try: 
			removetx_results_data = requests.get(this_endpoint).content
		except Exception as e:
			print(str(e))
			error=True
		else : 
			stringified = removetx_results_data.decode('utf-8')
			print(stringified)
			sanitized = json.loads(stringified)
			print(sanitized)
			if "error" in sanitized.keys() : 
				error = True 
	else :
		sanitized = { "Error" : True }
		error = True
	
	return render_template('display/Dremovetx_results.html.jinja', error=error, results=sanitized, txid=txid )


