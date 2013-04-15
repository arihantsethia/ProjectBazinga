# admin_views.py : Handles the views for Admin Module

from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, Blueprint
from time import gmtime, strftime
import bw

#Defining the Blueprint for admin_views.py
admin_views = Blueprint('admin_views',__name__)
# configuration

#This function sets the database connection
def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect('database.db')
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db
	return top.sqlite_db


@admin_views.route('/admin', methods=['GET', 'POST'])
def admin_login():
	error = None 
	message = None
	if request.method == 'POST':
		flag=0
		db = get_db()
		cur = db.execute('select * from admins')
		rows = cur.fetchall()	
		for row in rows:			
			if row[1]==request.form['username'] and row[2]==request.form['password']:				
				userid=row[0]
				username=row[1]
				flag=1
				break			
		if flag==0:
			error = 'Invalid username or password'
			flash('Invalid username or password')
			session['admin_logged_in'] = False
			session['admin_username'] = ''
			session['admin_userId'] = None
		else:
			error = 0
			session['admin_logged_in'] = True
			session['admin_username'] = username
			session['admin_userId'] = userid
			message = "Admin Logged in succesfully"	
		return render_template('admin.html',error=error,message=message)
	return render_template('admin.html')

@admin_views.route('/admin/contest',methods=['POST','GET'])
def contestadd():
	if request.method == 'POST' :
			db = get_db()
			db.execute('insert into contest (start_time , end_time, name, company, short_description, long_description, owner) values (?, ?, ?, ?, ?, ?, ?)',[request.form['start-time'], request.form['end-time'], request.form['contestname'], request.form['company'],request.form['shortdesc'],request.form['longdesc'],session['admin_username']])
			db.commit()
			message = "Congratulations "+" Your contest "+request.form['contestname']+" has been added "
			return render_template('admin.html' , message=message )
	return render_template('admin.html')


@admin_views.route('/addquestion',methods=['POST','GET'])
def contestadd():
    return render_template('addquestion.html')







