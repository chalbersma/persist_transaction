#!/usr/bin/env python3

"""
```swagger-yaml
/txid/{txid} :                                              
  get:                                               
    produces:                                        
      - application/json                             
    description: |                                   
      Grab Generic Data About a tracked Transaction ID
    responses:                                       
      200:                                           
        description: OK
    parameters:
      - name: txid
        in: path
        description: |
          Find latest info about tracked transaction id
        required: true
        type: string
                                  
```
"""

from flask import current_app, Blueprint, g, request, jsonify
import json
import ast
import time
import subprocess

txid = Blueprint('api_txid', __name__)

@txid.route("/txid/<str:txid>")
@txid.route("/txid/<str:txid>/")
def api_txid():

	root_meta_dict = dict()
	root_data_dict = dict()
	root_links_dict = dict()

	root_meta_dict["version"] = 1
	root_meta_dict["name"] = "txid"
	root_meta_dict["state"] = "In Progress"
	
	root_data_dict["electrum_synced"] = synced

	return jsonify(data=root_data_dict, meta=root_meta_dict, links=root_links_dict)
