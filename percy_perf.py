#!/usr/bin/env python3

import time
import argparse
from configparser import ConfigParser
import ast
import pymysql
import re
import json
import sys

# Our Stuff
from strans import strans

# Import Performance Checks
from perf import count_active_transactions
from perf import rclosed_tx
from perf import ractions
from perf import newtx
from perf import oldtx
from perf import atx_size
from perf import rtx_size

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("action",  nargs='+', help=("Thing you wish to check"))
	parser.add_argument("-c", "--configfile", help="Config File for Scheduler", required=True)
	parser.add_argument("-V", "--verbose", action="store_true", help="Enable Verbose Mode")
	parser._optionals.title = "DESCRIPTION "

	args = parser.parse_args()
	
	if args.action :
		ACTIONS = args.action

	CONFIG=args.configfile
	VERBOSE=args.verbose
	
def perf_check(CONFIG, ACTIONS, VERBOSE=False):
	
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
	
	db_conn = conn_db(config_items, VERBOSE)
	db_cur = db_conn.cursor(pymysql.cursors.DictCursor)
	
	# Electrum Up and Running
	# electrum daemon status | jq '.connected'
	
	directive = ACTIONS[0]
	modifiers = ACTIONS[1:]
	
	#print(directive, modifiers)
	
	known_commands = ["count_active_transactions", "rclosed_tx", "ractions", "newtx", "oldtx", "atx_size","rtx_size"]
	
	if directive in known_commands :
		this_function = globals()[directive]
		response=this_function.mainactions(args_list=modifiers, configs=CONFIG, db_cur=db_cur)
	else :
		response=( "Unknown:  Command :  " + str(directive) , 3 )
		
	return response
		
	

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
	results = perf_check(CONFIG, ACTIONS, VERBOSE=VERBOSE)
	
	print(results[0])
	sys.exit(results[1])
