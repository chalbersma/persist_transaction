#!/usr/bin/env python3

from configparser import ConfigParser 
from colorama import Fore, Back, Style
import time
import argparse
import ast
import pymysql

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--config", help="JSON Config File with our Storage Info", required=True)
	parser.add_argument("-V", "--verbose", action="store_true", help="Enable Verbose Mode")
	parser._optionals.title = "DESCRIPTION "

	# Parser Args
	args = parser.parse_args()

	# Grab Variables
	CONFIG=args.config
	VERBOSE=args.verbose
	
def archive_collections(CONFIG, VERBOSE) :

	# Process Config
	try:
		# Read Our INI with our data collection rules
		config = ConfigParser()
		config.read(CONFIG)
	except Exception as e: # pylint: disable=broad-except, invalid-name
		sys.exit('Bad configuration file {}'.format(e))

	# Grab me Collections Items Turn them into a Dictionary
	config_items=dict()

	# Collection Items
	for section in config :
		config_items[section]=dict()
		for item in config[section]:
			config_items[section][item] = config[section][item]
			
	if VERBOSE:
		print("Config Items: ", config_items)

	do_archive = True
	
	try : 
		# Note that Autocommit is off
		db_conn = pymysql.connect(host=config_items["db"]["dbhostname"], port=int(config_items["db"]["dbport"]), \
															user=config_items["db"]["dbuser"], passwd=config_items["db"]["dbpassword"], \
															db=config_items["db"]["dbname"], autocommit=True )
	except Exception as e :
		# Error
		print("Error Connecting to Datbase with error: ", str(e) )
		do_archive = False
		
	if do_archive == True :
		
		# Set Archive Time
		ARCHIVE_TIME = int(time.time())
		
		if VERBOSE:
			print("Archive Time: " , str(ARCHIVE_TIME))
		
		# Create Query Strings
		grab_delete_ids = "select id from trked_trans where active = False and lastChecked < FROM_UNIXTIME(" + str(ARCHIVE_TIME) +" ) - interval 7 DAY ;"
		
		remove_trked_trans_sql = "DELETE FROM trked_trans where id = %s ; "									
		
		remove_attempt_sql = "DELETE FROM attempts where fk_trked_trans_id = %s ; "

		cur = db_conn.cursor()
		
		if VERBOSE:
			print(grab_delete_ids)
			print(populate_archive_sql)
			print(remove_overachieving_sql)
		
		success = True
		
		try:
			cur.execute(grab_delete_ids)
			to_delete_ids=cur.fetchall()
		except Exception as e :
			if VERBOSE:
				print(Fore.RED, "Trouble with id grabbing query ", str(grab_delete_ids) , " error : ", str(e), Style.RESET_ALL)
			success = False
		else : 
			# Worked So Do the 
			try :
				cur.execute(remove_trked_trans_sql, to_delete_ids)
				trans_removed = cur.rowcount
				cur.execute(remove_attempt_sql, to_delete_ids)
				attempts_removed = cur.rowcount
			except Exception as e :
				if VERBOSE: 
					print(Fore.RED, "Trouble with removal queries error : ", str(e), Style.RESET_ALL)
				success = False
		
		if success == True :
			print(Fore.GREEN, "Long Transaction Archived", str(trans_removed), " | Attempt records removed ", str(attempts_removed), Style.RESET_ALL)
		else :
			print(Fore.RED, "Archiving has failed" , Style.RESET_ALL)

if __name__ == "__main__":
	archive_collections(CONFIG, VERBOSE)
