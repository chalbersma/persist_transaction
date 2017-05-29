#!/usr/bin/env python3

# Count Active Transactions

import pymysql

def mainactions(args_list, configs, db_cur) :
	# Count Active Transactions
	help_string='''
Usage:
* Default: Returns the number of currently opened & tracked transaction
           Specify the Warning and Critical Thresholds as the next two
           variables (or I'll use the default 50 100'''

	unknown_error=False
	warn = 50
	crit = 100
	
	#print(args_list)
	
	if len(args_list) == 2 : 
		# I've been provided Custom Warn's & Crits
		warn = int(args_list[0])
		crit = int(args_list[1])
	
	#print(warn, crit)
	
	total_transactions_query = "select count(*) as count from trked_trans where active = true ;"
	
	try:
		db_cur.execute(total_transactions_query)
	except Exception as e :
		unknown_error=True
		response_string = "UNKNOWN: MySQL Query Error " + str(e) 
		response_code = 3
		active_transactions = 0
	else:
		query_results = db_cur.fetchone()
		active_transactions = query_results["count"]
		if active_transactions > crit : 
			response_string = "CRITICAL: Large Number of Transactions " + str(active_transactions)
			response_code = 2
		elif active_transactions > warn : 
			response_string = "WARNING: Large Number of Transactions " + str(active_transactions)
			response_code = 1
		else : 
			# Number is okay
			response_string = "OK: Acceptable Number of Transactions " + str(active_transactions)
			response_code = 0
			
	perf_strings = list()
	perf_strings.append(" active_transactions="+str(active_transactions))
	
	perf_string = " | " + " , ".join(perf_strings)
	
	response_message = response_string + perf_string
	
	nag_object = ( response_message, response_code )
	
	return nag_object

