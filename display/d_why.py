from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Dwhy = Blueprint('display_why', __name__)

@Dwhy.route("/Dwhy/")
@Dwhy.route("/Dwhy/")
def display_why():
	
	return render_template('display/Dwhy.html.jinja')
