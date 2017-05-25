from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dhowto = Blueprint('display_howto', __name__)

@Dhowto.route("/Dhowto/")
@Dhowto.route("/Dhowto/")
def display_howto():
	
	return render_template('display/Dhowto.html.jinja')
