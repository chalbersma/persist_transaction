from flask import current_app, Blueprint, g, request, jsonify, render_template
import json
import ast
import requests


Daddemail = Blueprint('display_addemail', __name__)

@Daddemail.route("/Daddemail/")
@Daddemail.route("/Daddemail/")
def display_addemail():
	
	return render_template('display/Daddemail.html.jinja')

