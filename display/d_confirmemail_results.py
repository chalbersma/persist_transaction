from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dconfirmemail_results = Blueprint('display_confirmemail_results', __name__)

@Dconfirmemail_results.route("/Dconfirmemail_results/", methods=['GET'])
@Dconfirmemail_results.route("/Dconfirmemail_results/", methods=['GET'])
def display_confirmemail_results(emailid=None, confirmstring=None):
	
	error = False
	
	if "emailid" in request.args : 
		email = str(request.args["emailid"])
	
	if "confirmstring" in request.args : 
		confirmstring = str(request.args["confirmstring"])
	
	if email != None : 
		call_var = "?emailid=" + str(email) + "&confirmstring=" + str(confirmstring)
	else : 		
		error = True
	
	print(call_var)
	
	if error != True : 	
		this_endpoint = g.config_items["self"]["url"] + "api/confirmemail/" + call_var
	
		try: 
			addemail_results_data = requests.get(this_endpoint).content
		except Exception as e:
			print(str(e))
			
		stringified = addemail_results_data.decode('utf-8')
		sanitized = json.loads(stringified)
		if "error" in sanitized.keys() : 
			error = True 
	else :
		sanitized = { "Error" : True }
		error = True
	
	return render_template('display/Daddemail_results.html.jinja', error=error, results=sanitized )


