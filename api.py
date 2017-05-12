#!/usr/bin/env python3

from configparser import ConfigParser
import argparse
from flask import Flask, current_app, g, request, render_template
from flask_cors import CORS, cross_origin
import pymysql
import json
import ast
import time
import datetime
import os

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--configfile", help="Config File for Scheduler", required=True)
	parser.add_argument("-d", "--flaskdebug", action='store_true', help="Turn on Flask Debugging")
	parser._optionals.title = "DESCRIPTION "

	args = parser.parse_args()

	FDEBUG=args.flaskdebug
	CONFIG=args.configfile


def ui(CONFIG, FDEBUG):
	
	try:
		# Read Our INI with our data collection rules
		config = ConfigParser()
		config.read(CONFIG)
		# Debug
		#for i in config : 
			#for key in config[i] : 
				#print (i, "-", key, ":", config[i][key])
	except Exception as e: # pylint: disable=broad-except, invalid-name
		sys.exit('Bad configuration file {}'.format(e))

	

	# Grab me Collections Items Turn them into a Dictionary
	config_items=dict()

	# Collection Items
	for section in config :
		config_items[section]=dict()
		for item in config[section]:
			config_items[section][item] = ast.literal_eval(config[section][item])
	
	# Create db_conn
	
	app = Flask(__name__)

	# Enable CORS for UI Guys
	cors = CORS(app, resources={r"/(api)/*": {"origins": "*"}})


	@app.before_request
	def before_request():
	
		# DEFAULT Fresh. Use this instead of "Fresh" Values to allow for query caching.
		NOW = int(time.time())
		g.config_items = config_items
		
		try : 
			db_conn = pymysql.connect(host=config_items["db"]["dbhostname"], port=int(config_items["db"]["dbport"]), user=config_items["db"]["dbuser"], passwd=config_items["db"]["dbpassword"], db=config_items["db"]["dbname"], autocommit=True )
			g.db = db_conn

		except Exception as e : 
			print("Error connecting to database", str(e))
                
		g.cur = g.db.cursor(pymysql.cursors.DictCursor)
		
       
	@app.after_request
	def after_request(response) :
		# Close My Cursor JK Do that in teardown request
		return response
                
	@app.teardown_request
	def teardown_request(response):
		# Get Rid of My Cursor
		cur = getattr(g, 'cur', None)
		if cur is not None:
			cur.close()
			db = getattr(g, 'db', None)
		if db is not None:
			db.close()
		
		return response


	## API 2 Imports
	from api import root
	from api import synced
	from api import addtrans
	from api import txid
	from api import attempts
	from api import txlist
	from api import addcontact
	from api import confirmemail
	from api import watchtx
	
	# Register API Blueprints for Version 2
	app.register_blueprint(root.root, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(synced.synced, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(addtrans.addtrans, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(txid.txid, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(attempts.attempts, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(txlist.txlist, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(addcontact.addcontact, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(confirmemail.confirmemail, url_prefix=config_items["api"]["application_prefix"])
	app.register_blueprint(watchtx.watchtx, url_prefix=config_items["api"]["application_prefix"])
	
	## Display Imports
	from display import d_txid
	from display import d_txlist
	from display import d_addemail
	from display import d_addemail_results
	from display import d_confirmemail
	from display import d_confirmemail_results
	from display import d_addtx
	from display import d_addtx_results
	from display import d_watchtx_results
	
	# Register Display Blueprints
	app.register_blueprint(d_txid.Dtxid, url_prefix="/display")
	app.register_blueprint(d_txlist.Dtxlist, url_prefix="/display")
	app.register_blueprint(d_addemail.Daddemail, url_prefix="/display")
	app.register_blueprint(d_addemail_results.Daddemail_results, url_prefix="/display")
	app.register_blueprint(d_confirmemail.Dconfirmemail, url_prefix="/display")
	app.register_blueprint(d_confirmemail_results.Dconfirmemail_results, url_prefix="/display")
	app.register_blueprint(d_addtx.Daddtx, url_prefix="/display")
	app.register_blueprint(d_addtx_results.Daddtx_results, url_prefix="/display")
	app.register_blueprint(d_watchtx_results.Dwatchtx_results, url_prefix="/display")


	@app.route("/")
	def index():
		# Index
		return render_template("index.html.jinja")
	
	app.run(debug=FDEBUG, port=int(config_items['api']['port']) , threaded=True, host=config_items['api']['bindaddress'])
	

			
# Run if Execute from CLI
if __name__ == "__main__":
	ui(CONFIG, FDEBUG)
