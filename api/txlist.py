#!/usr/bin/env python3

"""
```swagger-yaml
/txlist :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
			Grab transaction list
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: inactive
        in: query
        description: |
          Include no longer tracked transactions.
        required: false
        type: string
      - name: amount
        description: |
				  Include only X amount of transactions By Default Limited to 100.
				required: false
				type: string
                                  
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess
import pymysql

txlist = Blueprint('api_txlist', __name__)

@txlist.route("/txlist", methods=['GET'])
@txlist.route("/txlist/", methods=['GET'])
def api_txlist(inactive=None, amount=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "txid"
	root_meta_dict["state"] = "In Progress"
	
	#root_data_dict["dbid"] = dbid
	#root_data_dict["txid"] = txid
	active_string = "where active = TRUE "
	# Default Limit
	limit=100
	do_query=True
	error=True
	
	if "inactive" in request.args :
		inactive = request.args["inactive"]
	elif "amount" in request.args :
		amount = int(request.args["amount"])
	
	if inactive != None :
		# No Inactive Specified
		active_string = "  "
	elif amount != None and type(amount) is int and amount > 1 :
		limit=int(amount)
		
	print(limit)
	
	
	if do_query == True :
		
		get_active_transactions = " SELECT id, txid, firstSeen, lastchecked, active FROM trked_trans " + active_string + "limit " + str(limit)
		
		try:
			g.cur.execute(get_active_transactions)
			print(get_active_transactions)
			howmany = g.cur.rowcount
			if (howmany == 0 ):
				# No Transaction
				error=True
				root_error_dict["notransaction"] = True
			else :
				transaction = g.cur.fetchall()
				howmany = g.cur.rowcount
				root_meta_dict["totaltx"] = howmany
				root_data_dict["data"] = list()
				for i in range(0, howmany):
					this_transaction = dict()
					this_transaction["attributes"] = transaction[i]
					this_transaction["id"] = transaction[i]["id"]
					root_data_dict["data"].append(this_transaction)
					
				root_data_dict["success"] = True
				error=False
		except pymysql.IntegrityError as e :
			root_error_dict["success"] = False
			root_error_dict["failure_message"] = "Integrity Error"
			root_error_dict["debug"] = str(e)
		except pymysql.ProgrammingError as e :
			root_error_dict["success"] = False
			root_error_dict["failure_message"] = "ProgrammingError"
			root_error_dict["debug"] = str(e)
		except pymysql.DataError as e :
			root_error_dict["success"] = False
			root_error_dict["failure_message"] = "DataError"
			root_error_dict["debug"] = str(e)
		except pymysql.NotSupportedError as e :
			root_error_dict["success"] = False
			root_error_dict["failure_message"] = "NotSupportedError"
			root_error_dict["debug"] = str(e)
		except pymysql.OperationalError as e :
			root_error_dict["success"] = False
			root_error_dict["failure_message"] = "OperationalError"
			root_error_dict["debug"] = str(e)	
		except Exception as e :
			root_error_dict["success"] = False
			root_error_dict["failure_short"] = "Unknown Failure " + str(e)
		
	if error : 
		# Return Error dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
