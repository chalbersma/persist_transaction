from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Daddemail_results = Blueprint('display_addemail_results', __name__)

@Daddemail_results.route("/Daddemail_results/", methods=['GET', 'POST'])
@Daddemail_results.route("/Daddemail_results/", methods=['GET', 'POST'])
def display_addemail_results(email=None, method=None):
	
	error = False
	
	if "email" in request.args : 
		email = str(request.args["email"])
	
	if "email" in request.form : 
		email = str(request.form["email"])
	
	if email != None : 
		call_var = "?email=" + str(email)
	else : 		
		error = True
	
	if error != True : 	
		this_endpoint = g.config_items["self"]["url"] + "api/addcontact/" + call_var
	
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


