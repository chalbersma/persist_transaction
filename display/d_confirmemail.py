from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dconfirmemail = Blueprint('display_confirmemail', __name__)

@Dconfirmemail.route("/Dconfirmemail/", methods=['GET'])
@Dconfirmemail.route("/Dconfirmemail/", methods=['GET'])
def display_confirmemail(emailid=None, confirmstring=None):
	
	error = False
	call_var = "?"
	
	if "emailid" in request.args : 
		try: 
			emailid = int(request.args["emailid"])
		except Exception as e :
			error = True
			root_error_dict["email_id_error"] = str(e)
			
		
	if "confirmstring" in request.args : 
		confirmstring = str(request.args["confirmstring"])	
		
	if emailid != None and confirmstring != None :
		# Add my query string
		call_var = call_var + "emailid=" + emailid + "&confirmstring=" + confirmstring
	else:
		error = True
	
	if error != True : 	
		this_endpoint = g.config_items["self"]["url"] + "api/confirmemail/" + call_var
	
		try: 
			confirmemail_data = requests.get(this_endpoint).content
		except Exception as e:
			print(str(e))
			
		stringified = confirmemail_data.decode('utf-8')
		sanitized = json.loads(stringified)
		if error in sanitized.keys() : 
			error = True 
	else :
		sanitized = { "Error" : True }
		error=True
	
	return render_template('display/Dconfirmemail.html.jinja', error=error, results=sanitized )


