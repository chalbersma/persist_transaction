#!/usr/bin/env python3

"""
```swagger-yaml
/root/ :                                              
  x-cached-length: "Every Midnight"                  
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Root endpopnt. Just an Info Point
    responses:                                       
      200:                                           
        description: OK                              
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time

root = Blueprint('api_root', __name__)

@root.route("/")
@root.route("/root")
@root.route("/root/")
def api_root():

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "Persistent Transaction"
	root_meta_dict["state"] = "In Progress"

	return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
