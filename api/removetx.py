#!/usr/bin/env python3

"""
```swagger-yaml
/removetx/ :                                              
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
        in: query
        description: |
          Txid to remove.
        required: true
        type: string
      - name: confirmstring
        in: query
        description: |
          The confirmation string given on transaction acceptance.
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
import uuid
import smtplib
from email.mime.text import MIMEText


removetx = Blueprint('api_removetx', __name__)

@removetx.route("/removetx", methods=['GET'])
@removetx.route("/removetx/", methods=['GET'])
def api_removetx(txid=None, confirmstring=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "removetx"
	root_meta_dict["state"] = "In Progress"
	
	error = False
	
	if "txid" in request.args : 
		txid = str(request.args["txid"])
	
	if "confirmstring" in request.args : 
		confirmstring = str(request.args["confirmstring"])
	
	if txid == None :
		# No Email Given
		error=True
		root_error_dict["Error"] = "No Email Given"
	elif confirmstring == None : 
		error=True
	else :
		# Grab 
		transaction_get_query = "select * from trked_trans where active = TRUE and txid = '" + txid + "' ; "
		try:
			g.cur.execute(transaction_get_query)
			howmany = g.cur.rowcount
			if (howmany > 0 ):
				# Transaction is in System
				transaction_exists = True
				fromDB = g.cur.fetchone()
			else : 
				# No Such Transaction in System
				error=True
				transaction_exists = False
				root_error_dict["no_transaction"] = True
		except Exception as e :
			error=True
			root_error_dict["success"] = False
			root_error_dict["failure_short"] = "Unknown Failure " + str(e)
		else : 
			if transaction_exists == True : 
				if fromDB["deletestring"] == "none" or fromDB["deletestring"] != confirmstring : 
					# Removal String Doesn't Match
					error=True
					root_error_dict["no_transaction"] = False
					root_error_dict["mismatch_confirm_string"] = True
				else : 
					# Removal String Matches Remove & Retire
					this_transaction = strans(txid=fromDB["txid"], txhex=fromDB["hextx"], dbid=fromDB["id"], electrum_string=g.config_items["electrum"]["electrum_command"])
					
					updatedict = dict()
					updatedict["result"] = "retirement"
					updatedict["still_valid"] = "false"
					
					update_results = this_transaction.do_update(g.cur, updatedict)
					
					if update_results["success"] == True : 
						# Successful
						root_meta_dict["update_success"] = update_results
						# Go Through Nofity Process if there's an attached Email
						this_transaction_nofity = this_transaction.retire_notify(g.cur, g.config_items["email"], g.config_items["self"]["url"])
						root_data_dict["notify_results"] = this_transaction_nofity
					else : 
						# Failed
						error = True
						root_error_dict["update_error"] = "Error Updating Transaction with Retirement."
					
			
	if error :
		# Error Return Dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# We're Good Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
