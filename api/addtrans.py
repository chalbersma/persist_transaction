#!/usr/bin/env python3

"""
```swagger-yaml
/addtrans/{txid} :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Grab Generic Data About a tracked Transaction ID
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: txid
        in: path
        description: |
          Add an unconfirmed transaction to the check
        required: true
        type: string
                                  
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess
from strans import strans
import subprocess


addtrans = Blueprint('api_addtrans', __name__)

@addtrans.route("/addtrans/<string:txid>")
@addtrans.route("/addtrans/<string:txid>/")
def api_addtrans(txid="none"):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "addtrans"
	root_meta_dict["state"] = "In Progress"
	
	error = False
	
	transaction = strans(txid, electrum_string=g.config_items["electrum"]["electrum_command"])
	valid = transaction.check_still_valid()
	
	if valid[0] == True : 
		# Transaction is Still Valid, Add to DB
		result = transaction.add_to_database(g.cur)
		if result["success"] == True :
			# Successfully Added to Tracker
			root_data_dict["result"] = result
		else :
		  # Failure
		  error = True
		  root_error_dict["result"] = result
	else :
		# Transaction invalid
		error = True
		root_error_dict["invalid_transaction"] = True
		root_error_dict["invalid_transaction_message"] = str(valid[1])
	
	if error :
		# Error Return Dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# We're Good Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
