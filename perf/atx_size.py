#!/usr/bin/env python3

# Size of Active Transactions

import pymysql

def mainactions(args_list, configs, db_cur) :
	help_string='''
Usage:
* Default: Returns the average size of active transactions in KB. 
	By Default Warn Crit Time is the format for
  customization otherwise it's 50KB / 100KB'''

	unknown_error=False
	warn = 50
	crit = 100
	
	#print(args_list)
	
	if len(args_list) > 2 : 
		# I've been provided Custom Warn's & Crits
		warn = int(args_list[0])
		crit = int(args_list[1])
	
	atxsize_query = "select AVG(length(hextx))/1024 as size from trked_trans where active = true ;"
	
	try:
		db_cur.execute(atxsize_query)
	except Exception as e :
		unknown_error=True
		response_string = "UNKNOWN: MySQL Query Error " + str(e) 
		response_code = 3
		avg_size = 0
	else:
		query_results = db_cur.fetchone()
		avg_size = query_results["size"]
		if avg_size > crit : 
			response_string = "CRITICAL: Size of Transactions : " + str(round(avg_size,2)) + "KB"
			response_code = 2
		elif avg_size > warn : 
			response_string = "WARNING: Size of Transactions : " + str(round(avg_size,2)) + "KB"
			response_code = 1
		else : 
			# Number is okay
			response_string = "OK: Size of Transactions :  " + str(round(avg_size,2)) + "KB"
			response_code = 0
			
	perf_strings = list()
	perf_strings.append("avg_size="+str(avg_size))
	
	perf_string = " | " + " , ".join(perf_strings)
	
	response_message = response_string + perf_string
	
	nag_object = ( response_message, response_code )
	
	return nag_object

