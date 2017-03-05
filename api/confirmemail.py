#!/usr/bin/env python3

"""
```swagger-yaml
/confirmemail/ :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Adds an email and triggers off a confirmation email.
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: emailid
        in: query
        description: |
          Add an email to the tracking.
        required: true
        type: int
      - name: confirmstring
        in: query
        description: |
          How to send. Currenlty only email supported. Currently ignored
          until more than email is supported.
        required: false                              
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess
from strans import strans
import subprocess


confirmemail = Blueprint('api_confirmemail', __name__)

@confirmemail.route("/confirmemail", methods=['GET'])
@confirmemail.route("/confirmemail/", methods=['GET'])
def api_confirmemail(emailid=None, confirmstring=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "confirmemail"
	root_meta_dict["state"] = "In Progress"
	
	error = False
	
	print(request.args)
	
	if "emailid" in request.args : 
		try: 
			emailid = int(request.args["emailid"])
		except Exception as e :
			error = True
			root_error_dict["email_id_error"] = str(e)
		
	if "confirmstring" in request.args : 
		confirmstring = str(request.args["confirmstring"])	
	
	if emailid == None or confirmstring == None : 
		error = True
		root_error_dict["variable_error"] = "Either no emailid or no confirmstring"
	
	if error == False :
		
		grab_confirm = " select confirmstring from emails where emailid = " + str(emailid)
	
	try:
		g.cur.execute(grab_confirm)
		howmany = g.cur.rowcount
		print(howmany)
		if (howmany != 1 ):
			# No Transaction
			error=True
			root_error_dict["notransaction"] = True
		else :
			fromDB = g.cur.fetchone()
	except Exception as e :
		error = True
		root_error_dict["error"] = "Error doing query"
	else:		
		if confirmstring == fromDB["confirmstring"] :
			# Email is Confirmed
			root_data_dict["confirmation_matches"] = True
			
			update_query = "update emails set active = 1 where emailid = " + str(emailid) + " limit 1 "
			
			try:
				g.cur.execute(update_query)
				root_data_dict["dbupdated"] = True
			except Exception as e :
				error = True
				root_error_dict["dbupdateerror"] = True
			
		else :
			root_error_dict["confirmation_matches"] = False
			error = True
			
		
			
			
	if error :
		# Error Return Dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# We're Good Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
