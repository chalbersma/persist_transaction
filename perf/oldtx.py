#!/usr/bin/env python3

# Old Transactions

import pymysql

def mainactions(args_list, configs, db_cur) :
	help_string='''
Usage:
* Default: Returns the number of old, active transactions
 (By Default 1 Day). By Default Warn Crit Time is the format for
  customization otherwise it's 50/100'''

	unknown_error=False
	warn = 50
	crit = 100
	hours = 24
	
	#print(args_list)
	
	if len(args_list) > 2 : 
		# I've been provided Custom Warn's & Crits
		warn = int(args_list[0])
		crit = int(args_list[1])
	if len(args_list) == 3 : 
		# I've additionally been provided a custom date range.
		hours = int(args_list[2])
	
	query_args = [ hours ]
	oldtx_query = "select count(*) as count from trked_trans where active = true and firstseen < NOW() - INTERVAL %s HOUR ; "
	
	try:
		db_cur.execute(oldtx_query, query_args)
	except Exception as e :
		unknown_error=True
		response_string = "UNKNOWN: MySQL Query Error " + str(e) 
		response_code = 3
		newtxs = 0
	else:
		query_results = db_cur.fetchone()
		oldtxs = query_results["count"]
		if oldtxs > crit : 
			response_string = "CRITICAL: Large Number of Old Transactions " + str(oldtxs)
			response_code = 2
		elif oldtxs > warn : 
			response_string = "WARNING: Large Number of Old Transactions " + str(oldtxs)
			response_code = 1
		else : 
			# Number is okay
			response_string = "OK: Acceptable Number of Old Transactions " + str(oldtxs)
			response_code = 0
			
	perf_strings = list()
	perf_strings.append("oldtxs="+str(oldtxs))
	
	perf_string = " | " + " , ".join(perf_strings)
	
	response_message = response_string + perf_string
	
	nag_object = ( response_message, response_code )
	
	return nag_object

