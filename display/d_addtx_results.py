from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests

# Results of Attempting to Add Transaction.

Daddtx_results = Blueprint('display_addtx_results', __name__)

@Daddtx_results.route("/Daddtx_results/", methods=['GET', 'POST'])
@Daddtx_results.route("/Daddtx_results/", methods=['GET', 'POST'])
def display_addtx_results(txid=None, method=None):
	
	error = False
	
	if "txid" in request.args : 
		txid = str(request.args["txid"])
	
	if "txid" in request.form : 
		txid = str(request.form["txid"])
	
	if txid == None : 
		error = True
	
	if error != True : 	
		this_endpoint = g.config_items["self"]["url"] + "api/addtrans/" + str(txid)
	
		try: 
			addtx_results_data = requests.get(this_endpoint).content
		except Exception as e:
			print(str(e))
			error=True
		else : 
			stringified = addtx_results_data.decode('utf-8')
			print(stringified)
			sanitized = json.loads(stringified)
			print(sanitized)
			if "error" in sanitized.keys() : 
				error = True 
	else :
		sanitized = { "Error" : True }
		error = True
	
	return render_template('display/Daddtx_results.html.jinja', error=error, results=sanitized, txid=txid )


