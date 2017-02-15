#!/usr/bin/env python3

"""
```swagger-yaml
/txid/{txid} :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Grab Generic Data About a tracked by transactiona id.
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: txid
        in: path
        description: |
          Find latest info about tracked transaction id
        required: true
        type: string
                                  
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess
import pymysql

txid = Blueprint('api_txid', __name__)

@txid.route("/txid/<string:txid>", methods=['GET'])
@txid.route("/txid/<string:txid>/", methods=['GET'])
@txid.route("/txid/<int:dbid>", methods=['GET'])
@txid.route("/txid/<int:dbid>/", methods=['GET'])
def api_txid(txid=None, dbid=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "txid"
	root_meta_dict["state"] = "In Progress"
	
	#root_data_dict["dbid"] = dbid
	#root_data_dict["txid"] = txid
	where_string = str()
	do_query=False
	error=True
	
	if dbid != None :
		# Given dbid use
		do_query = True
		where_string = " id = " + str(dbid) + " "
	elif txid != None and txid.isalnum() :
		do_query = True
		where_string = " txid = '" + str(txid) + "' "
	else :
		do_query = False
		# Error Incoming
		root_error_dict["inputerrors"] = "Given values do not make sense"
	
	if do_query == True :
		get_transaction_query = " SELECT * FROM trked_trans where " + where_string 
		print(get_transaction_query)
		
		try:
			g.cur.execute(get_transaction_query)
			howmany = g.cur.rowcount
			print(howmany)
			if (howmany != 1 ):
				# No Transaction
				error=True
				root_error_dict["notransaction"] = True
			else :
				transaction = g.cur.fetchone()
				root_data_dict["info"] = transaction
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
