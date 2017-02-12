#!/usr/bin/env python3

# Not an API Endpoint
import subprocess
import json
import pymysql


# Simple Transaction Class
class strans:
	
	def __init__(self, txid, txhex = None, dbid = None, electrum_string="electrum"):
		
		self.txhex = None
		self.txid = None
		self.dbid = None
		self.electrum = electrum_string
		
		if txhex == None : 
			# Wasn't given a transaction hex so I need to ask the network for it.
			if txid.isalnum() :
				# Build Transaction
				self.txid = txid
				electrum_command = self.electrum + " gettransaction " + txid
				
				try:
					raw_transaction_info = subprocess.check_output(electrum_command, shell=True)
				except Exception as e :
					print("Error with transaction", str(e))
					return
				
			else : 
				#print(txid)
				raise Exception("Bad Transaction")
				
			transaction_info = json.loads(raw_transaction_info.decode('utf-8'))
			#print(transaction_info)
			self.txhex = transaction_info["hex"]
		else:
			# Transaction Hex Given
			self.txid = txid
			self.txhex = txhex
		
		if dbid != None :
			self.dbid = int(dbid)
			
	def retire_in_db(self, dbconn) :
		
		retire_transaction_string = "UPDATE trked_trans set active = 0 where id = " + self.dbid
		
		try:
			dbconn.execute(retire_transaction_string)
			return_dict["success"] = True
		except pymysql.IntegrityError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "Integrity Error"
			return_dict["debug"] = str(e)
		except pymysql.ProgrammingError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "ProgrammingError"
			return_dict["debug"] = str(e)
		except pymysql.DataError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "DataError"
			return_dict["debug"] = str(e)
		except pymysql.NotSupportedError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "NotSupportedError"
			return_dict["debug"] = str(e)
		except pymysql.OperationalError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "OperationalError"
			return_dict["debug"] = str(e)	
		except Exception as e :
			return_dict["success"] = False
			return_dict["failure_short"] = "Unknown Failure " + str(e)
		
		return return_dict
			
	def do_update(self, dbconn, updatedict):
		return_dict = dict()
		
		do_update_sql = "INSERT into attempts (fk_trked_trans_id, result) VALUES (%s, %s) ; " +\
										"UPDATE trked_trans set lastChecked = CURRENT_TIMESTAMP, active = %s  where id = %s ; " 
		
		values_to_insert = (self.dbid, updatedict["result"], updatedict["still_valid"], self.dbid )
		
		try:
			dbconn.execute(do_update_sql, values_to_insert)
			return_dict["insert_id"] = dbconn.lastrowid
			self.dbid = int(return_dict["insert_id"])
			return_dict["success"] = True
		except pymysql.IntegrityError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "Integrity Error"
			return_dict["debug"] = str(e)
		except pymysql.ProgrammingError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "ProgrammingError"
			return_dict["debug"] = str(e)
		except pymysql.DataError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "DataError"
			return_dict["debug"] = str(e)
		except pymysql.NotSupportedError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "NotSupportedError"
			return_dict["debug"] = str(e)
		except pymysql.OperationalError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "OperationalError"
			return_dict["debug"] = str(e)	
		except Exception as e :
			return_dict["success"] = False
			return_dict["failure_short"] = "Unknown Failure " + str(e)
		
		return return_dict
	
	def check_still_valid(self):
		# Do the bits to check if the transaction is still valid (resubmit it).
		if self.txhex == None : 
			check_result=[ False, "No Transaction Hex (Maybe Transaction not in Mempool)" ]
		else:
			if self.txhex.isalnum():
				#print(self.txhex)
				electrum_check_valid = self.electrum +  " broadcast " + self.txhex
				try:
					raw_electrum_check = subprocess.check_output(electrum_check_valid, shell=True)
					check_result = json.loads(raw_electrum_check.decode('utf-8'))
				except Exception as e :
					check_result_dict = [ False, "Issue with Transaction: " + str(e)  ]
					check_result = json.loads(check_result_dict)
				
				
			else :
				raise Exception("Bad Hex Value")
			
		
		return check_result
		
	def add_to_database(self, dbconn):
		# Add to Database
		
		return_dict = dict()
		
		
		values_to_insert = (self.txid, True, self.txhex)
		add_transaction_string = "INSERT into trked_trans (txid, active, hextx) VALUES( %s, %s, %s ) ;"
		
		try:
			dbconn.execute(add_transaction_string, values_to_insert)
			return_dict["insert_id"] = dbconn.lastrowid
			self.dbid = int(return_dict["insert_id"])
			return_dict["success"] = True
		except pymysql.IntegrityError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "Integrity Error (Transaction probably already in system)"
			return_dict["debug"] = str(e)
		except pymysql.ProgrammingError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "ProgrammingError"
			return_dict["debug"] = str(e)
		except pymysql.DataError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "DataError"
			return_dict["debug"] = str(e)
		except pymysql.NotSupportedError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "NotSupportedError"
			return_dict["debug"] = str(e)
		except pymysql.OperationalError as e :
			return_dict["success"] = False
			return_dict["failure_message"] = "OperationalError"
			return_dict["debug"] = str(e)	
		except Exception as e :
			return_dict["success"] = False
			return_dict["failure_short"] = "Unknown Failure " + str(e)
		
		return return_dict
		
		
	def print_me(self) :
		print("My TXID: " , self.txid)
		print("My HEXID: " , self.txhex)
