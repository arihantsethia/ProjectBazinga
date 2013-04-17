# Main File : This has to be run to start the server
from __future__ import with_statement
from pqueue import priority_dict
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint, jsonify
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack
from Queue import PriorityQueue

import urllib
import urllib2

# Database Configuration
DATABASE = 'database.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

p = PriorityQueue()

def initp():
	global p
	p = priority_dict()
	p['http://localhost:2345'] = 0
	#print 'sdf'
	#print p.get()

@app.route('/', methods=['GET', 'POST'])
def getserver():
	#print 'dsf'
	#print p
	global p
	sm = p.smallest()
	p[sm] += 1
	if request.method=='POST':
		print request.form
		url = sm	#least loaded server
		values = {'qid' : request.form['qid'], 'code': request.form['code'], 'lang': request.form['lang'], 'user_id': request.form['user_id'] } 

		data = urllib.urlencode(values)
		response = urllib2.urlopen(url, data)
		page = response.read()
	return jsonify(server=sm)

if __name__ == '__main__':
	#init_db()
	initp()
	app.run(debug=True, port=1234)
	

