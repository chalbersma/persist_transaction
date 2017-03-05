#!/usr/bin/env python3

"""
```swagger-yaml
/watchtx/ :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Adds an email and triggers off a confirmation email.
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: txid
        in: path
        description: |
          Add an email to the tracking.
        required: true
        type: int
      - name: email
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
import re


watchtx = Blueprint('api_watchtx', __name__)

@watchtx.route("/watchtx", methods=['GET'])
@watchtx.route("/watchtx/", methods=['GET'])
def api_watchtx(txid=None, email=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "watchtx"
	root_meta_dict["state"] = "In Progress"
	
	error = False
		
	if "email" in request.args : 
		try: 
			email = str(request.args["email"])
		except Exception as e :
			error = True
			root_error_dict["email_error"] = str(e)
		else : 
			parse_email_pattern = re.compile(g.config_items["email"]["validation_regex"])
			valid = parse_email_pattern.match(email)
			
			if valid :
				# Pass email is good
				pass
			else :
				email = None
				root_error_dict["invalid_email"] = True
		
	if "txid" in request.args : 
		txid = str(request.args["txid"])	
	
	if email == None or txid == None : 
		error = True
		root_error_dict["variable_error"] = "Either no emailid or no transactionid"
	
	if error == False :
		
		grabemail = " select emailid from emails where email = '" + str(email) + "' and active = 1 limit 1"
		grabtxid = " select id from trked_trans where txid = '" + str(txid) + "' and active = 1 limit 1"
		
		try: 
			g.cur.execute(grabemail)
			emailid = g.cur.fetchone()
			g.cur.execute(grabtxid)
			dbtxid = g.cur.fetchone()
		except Exception as e :
			error = True
			root_error_dict["error"] = "Error with grabbing transactions: " + str(e)
		else :
			# Add Watchtx
			#print(dbtxid, emailid)
			watchtxquery = " replace into notify_lookup ( fk_trked_trans_id, fk_emailid ) values ( '" + str(dbtxid["id"]) + "' , '" + str(emailid["emailid"]) + "' ) "
			#print(watchtxquery)
			try:
				g.cur.execute(watchtxquery)
				watchid = g.cur.lastrowid
			except Exception as e :
				error=True
				root_error_dict["inserterror"] = "Error inserting transaction into notify_lookup : " + str(e)
			
	if error :
		# Error Return Dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# We're Good Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
