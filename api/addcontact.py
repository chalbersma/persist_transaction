#!/usr/bin/env python3

"""
```swagger-yaml
/addcontact/ :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Adds an email and triggers off a confirmation email.
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: contact
        in: query
        description: |
          Add an email to the tracking.
        required: true
        type: string
      - name: method
        in: query
        description: |
          How to send. Currenlty only email supported. Currently ignored
          until more than email is supported.
        required: false                              
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess
from strans import strans
import subprocess
import re
import uuid
import smtplib
from email.mime.text import MIMEText


addcontact = Blueprint('api_addcontact', __name__)

@addcontact.route("/addcontact", methods=['GET'])
@addcontact.route("/addcontact/", methods=['GET'])
def api_addcontact(email=None, method=None):

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()
	root_error_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "addcontact"
	root_meta_dict["state"] = "In Progress"
	
	error = False
	
	if "email" in request.args : 
		email = str(request.args["email"])
	
	if email == None :
		# No Email Given
		error=True
		root_error_dict["Error"] = "No Email Given"
	else :
		# Verify Email
		parse_email_pattern = re.compile(g.config_items["email"]["validation_regex"])
		valid = parse_email_pattern.match(email)
		if valid :
			# We've a valid email address
			check_if_email_query = "select emailid from emails where email = '" + email + "' ; "
			
			try:
				g.cur.execute(check_if_email_query)
				howmany = g.cur.rowcount
				if (howmany > 0 ):
					# Email in System
					email_exists=True
					error=True
					emailid = g.cur.fetchone()
					root_error_dict["preexisting_email"] = emailid
					root_error_dict["bademail"] = "Email already in system."					
			except Exception as e :
				error=True
				root_error_dict["success"] = False
				root_error_dict["failure_short"] = "Unknown Failure " + str(e)
			else : 
				# Email Not In System, Add Random String
				confirm_string = str(uuid.uuid4())
				insert_string="INSERT into emails (email, confirmstring, active) VALUES ('" + email + "', '" + confirm_string + "', 0 ) ; "
				
				try :
					g.cur.execute(insert_string)
					emailid = g.cur.lastrowid
				except Exception as e :
					error=True
					root_error_dict["insert_error"] = str(e)
					root_error_dict["failure"] = True
				else : 
					# Send Confirmation Email
					root_data_dict["emailid"] = int(emailid)
					root_data_dict["email"] = str(email)
					
					message_parts = list()
					message_parts.append("Hello,  ")
					message_parts.append("Please confirm your email, visit :")
					message_parts.append(" ")
					message_parts.append(g.config_items["self"]["url"] + "display/Dconfirmemail_results/?" + "emailid=" + str(emailid) + "&" + "confirmstring=" + str(confirm_string))
					
					message="\n".join(message_parts)
					
					msg = MIMEText(message)
					msg['From'] = g.config_items["email"]["fromemail"]
					msg['To'] = str(email)
					msg['Subject'] = "Percy: Confirm Your Email"
					
					mailserver = smtplib.SMTP(g.config_items["email"]["smtp_host"],g.config_items["email"]["smtp_port"])
					
					mailserver.ehlo()
					
					print(g.config_items["email"])
					
					if g.config_items["email"]["usetls"] == True :
						mailserver.starttls()
						mailserver.ehlo()
					
					if g.config_items["email"]["useuserauth"] == True :
						mailserver.login(g.config_items["email"]["smtpauthuser"], g.config_items["email"]["smtpauthpassword"])

					mailserver.sendmail(g.config_items["email"]["fromemail"],str(email),msg.as_string())

					mailserver.quit()
					
					pass
					

					
		else :
			error=True
			root_error_dict["Invalid_Email"] = "Invalid email"
	
	if error :
		# Error Return Dict
		return jsonify(error=root_error_dict, meta=root_meta_dict, links=root_links_dict)
	else :
		# We're Good Return Data
		return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
