# -*- coding: utf-8 -*-
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
import os , shutil

#Defining the Blueprint for views.py
login_views = Blueprint('login_views',__name__)
# configuration

def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect('database.db')
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db
	return top.sqlite_db 

@login_views.route('/login', methods=['GET', 'POST'])
def login():			#form validation using this function in signup.html
    error = None 
    message = None
    if request.method == 'POST':
		flag=0
		db = get_db()
		cur = db.execute('select * from users')
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
			session['logged_in'] = False
			session['username'] = ''
			session['userId'] = None
		else:
			error = 0
			session['logged_in'] = True
			session['username'] = username
			session['userId'] = userid
			message = "Logged in succesfully"			
		return render_template('index.html', error=error , message=message )

@login_views.route('/register' , methods=['POST','GET'])
def register():                    #renders the signup.html
	if request.method == 'POST' :
		db = get_db()
		cur = db.execute('select * from users where username=?',[request.form['username']]);
		cur = cur.fetchall()
		if (len(cur)>0) :
			error = "Username not available"
			return render_template('register.html' , error=error )
		else :
			print request.form['username']
			print request.form['password']
			print request.form['email']
			print request.form['name']
			db.execute('insert into users (username, password, email, name) values (?, ?, ?, ?)',[request.form['username'], request.form['password'], request.form['email'], request.form['name']])
			message = "Congratulations "+request.form['username']+", You are now a member of Bazinga Community "
			user = db.execute('select * from users where username=?',[request.form['username']])
			user = user.fetchone()
			shutil.copy2('static/files/default.jpg','static/files/'+str(user['user_id'])+'.jpg')
			db.commit()
			return render_template('index.html' ,  message=message )
	return render_template('register.html')

@login_views.route('/logout')
def logout():
	session.clear()
	message = "Logged out succesfully"
	return render_template('index.html' , message=message)

@login_views.route('/forgot', methods=['GET', 'POST'])
def forgot():
	message = None
	error = None
	if request.method == 'POST':
		print 'Message =' + request.form['username']	
		print 'Message =' + request.form['email']
		message = "An email has been sent to " + request.form['email']
	return render_template('forgot.html',  error=error ,message=message)

@login_views.route('/change', methods=['GET', 'POST'])
def change():
	message = None
	error = None
	if request.method == 'POST':
		db=get_db()
		cur=db.execute('select * from users where username=?',[request.form['username']])
		cur = cur.fetchone()
		if (len(cur)>0 and cur['password']==request.form['password']):
			db.execute('update users set password=? where username=?',[request.form['newpassword'],request.form['username']])
			message="Your password is changed successfully"
			db.commit()
			return render_template('index.html', message=message)
		else:
			error = "Please enter the corret username and password"
	return render_template('change.html', error=error , message=message)

def user(user_id):
	db = get_db()
	cur = db.execute('select * from users where user_id=?',[user_id])
	cur = cur.fetchone()
	return cur