# Views.py : Handles the views of general modules

from flask import Flask, render_template, redirect, url_for, Blueprint

#Defining the Blueprint for views.py
views = Blueprint('views',__name__)

@views.route('/')
def index():
	return render_template("index.html")

@views.route('/home')
def home():
	return render_template("index.html")



