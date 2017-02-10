#!/usr/bin/env python3

"""
```swagger-yaml
/synced/ :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Tells if electrum is synced
    responses:                                       
      200:                                           
        description: OK                              
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess

synced = Blueprint('api_synced', __name__)

@synced.route("/synced")
@synced.route("/synced/")
def api_synced():

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "Synced"
	root_meta_dict["state"] = "In Progress"
	
	root_meta_dict["Underlying Command"] = "electrum is_synchronized"

	synced = subprocess.getoutput(root_meta_dict["Underlying Command"])
	
	root_data_dict["electrum_synced"] = synced

	return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
