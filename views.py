# Views.py : Handles the views of general modules
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
import smtplib
#Defining the Blueprint for views.py
views = Blueprint('views',__name__)

@views.route('/')
def index():
	return render_template("index.html")

@views.route('/home')
def home():
	return render_template("index.html")

@views.route('/about')
def about():
	return render_template("about.html")

@views.route('/contact', methods=['GET', 'POST'])
def contact():
	if request.method == 'POST':
		email_to = "contact@bazinga.com"
		email_from = request.form['email']
		email_subject = request.form['subject']
		email_msg = request.form['msg']+'\n'+ request.form['firstname']+' '+request.form['lastname']
		#Define host to send mail
		#server = smtplib.SMTP(HOST)
		#server.sendmail(email_from, [email_to], email_msg)
		#server.quit()
		message = "Thank You for Contacting Us. We will soon get in touch with you."
		return render_template("index.html" , message = message)
	return render_template("contact.html")


