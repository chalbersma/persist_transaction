from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Daddtx = Blueprint('display_addtx', __name__)

@Daddtx.route("/Daddtx/")
@Daddtx.route("/Daddtx/")
def display_addtx():
	
	return render_template('display/Daddtx.html.jinja')

