#!/usr/bin/env python3

import time
import argparse
from configparser import ConfigParser
import ast
import pymysql
import re
import json

# Our Stuff
from strans import strans

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--configfile", help="Config File for Scheduler", required=True)
	parser.add_argument("-V", "--verbose", action="store_true", help="Enable Verbose Mode")
	parser._optionals.title = "DESCRIPTION "

	args = parser.parse_args()

	CONFIG=args.configfile
	VERBOSE=args.verbose
	
def process_transactions(CONFIG, VERBOSE=False):
	
	config_items = dict()
	
	try:
		# Try to Parse
		config = ConfigParser()
		config.read(CONFIG)
	except Exception as e: 
		# Error if Parse
		print("File ", CONFIG, " not paresed because of " , format(e))
		verified=False
	else:
        # It's good so toss that shit in
		for section in config :
			config_items[section]=dict()
			for item in config[section]:
				config_items[section][item] = ast.literal_eval(config[section][item])
				
	#print(config_items)
	
	db_conn = conn_db(config_items, VERBOSE)
	
	a_trans_data = grab_transactions(CONFIG, db_conn, VERBOSE)
	
	#print(a_trans_data)
	transaction_objects = list()
	how_many_transactions = a_trans_data[0]

	txresults = dict()
	txresults["resubmit"] = 0
	txresults["confirmed"] = 0
	txresults["invalid"] = 0
	txresults["retired"] = 0
	txresults["totaltrans"] = how_many_transactions

	if how_many_transactions > 0 :
		all_transactions = a_trans_data[1]
		for transaction in all_transactions:
			this_transaction = strans(txid=transaction["txid"], txhex=transaction["hextx"], dbid=transaction["id"])
			valid = this_transaction.check_still_valid()
			#print(valid)
			Update_Status = dict()
			if valid[0] == False :
				# No Longer Valid
				Update_Status["still_valid"] = False
				txresults["retired"] += 1
				
				confirmed = "already in block chain"
				if re.search(confirmed, valid[1]) != None  : 
					Update_Status["result"] = "confirmed"
					txresults["confirmed"] += 1
				else :
					Update_Status["result"] = "invalid"
					Update_Status["still_valid"] = False
					txresults["invalid"] += 1 
			else :
				# Still Valid
				Update_Status["still_valid"] = True
				Update_Status["result"] = "resubmit"
				txresults["resubmit"] += 1

			cur = db_conn.cursor(pymysql.cursors.DictCursor)
			
			this_transaction_update_results = this_transaction.do_update(cur, Update_Status)
			if VERBOSE:
				print(transaction["txid"], this_transaction_update_results)
			
			cur.close()
			
	
	return txresults
			
def grab_transactions(CONFIG, db_conn, VERBOSE=False):
	
	cur = db_conn.cursor(pymysql.cursors.DictCursor)
	
	grab_trans_query = " select * from trked_trans where active = TRUE and lastchecked <= ( NOW() - INTERVAL 6 HOUR ) "
	
	try:
		cur.execute(grab_trans_query)
	except Exception as e :
		print("Error finding transaction ", str(e) )
		active_transactions = 0
		all_transactions = list()
	else:
		if not cur.rowcount :
			# No Results
			all_transactions = list()
			active_transactions = 0
		else :
			all_transactions = cur.fetchall()
			active_transactions = len(all_transactions)
	
	
	cur.close()
	
	return ( active_transactions, all_transactions )
	

def conn_db(config_items, VERBOSE=False):
	
		# Grab the Currently Active Transactions from the Database
	try:
		db_conn = pymysql.connect(host=config_items["db"]["dbhostname"], port=int(config_items["db"]["dbport"]), user=config_items["db"]["dbuser"], passwd=config_items["db"]["dbpassword"], db=config_items["db"]["dbname"], autocommit=True )
		#dbmessage = "Good, connected to " + config_items["db"]["dbuser"]  + "@" + config_items["db"]["dbhostname"] + ":" + config_items["db"]["dbport"] + "/" + db=config_items["db"]["dbname"]
		
	except Exception as e:
		print("Database Error: ", str(e))
		db_conn = False
			
	return db_conn
	
if __name__ == "__main__":
	results = process_transactions(CONFIG, VERBOSE)
	
	results_json = json.dumps(results)
	
	print(results_json)
