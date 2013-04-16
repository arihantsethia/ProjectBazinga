# admin_views.py : Handles the views for Admin Module

from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, Blueprint
from datetime import datetime
<<<<<<< HEAD

=======
>>>>>>> 7843b6aad8d96e36d50dcc5f7c4ec4a275cdaf56

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
		cur = db.execute('SELECT * from admins WHERE username=?',[request.form['username']])
		row = cur.fetchone()	
		if row[2]==request.form['password']:				
			userid=row[0]
			username=row[1]
			session['admin_logged_in'] = True
			session['admin_username'] = username
			session['admin_userId'] = userid
			message = "Logged in succesfully"
		else:
			error = 'Invalid username or password'
			session['admin_logged_in'] = False
			session['admin_username'] = ''
			session['admin_userId'] = None		
		return render_template('admin.html',error=error,message=message)
	return render_template('admin.html',error=error)

@admin_views.route('/admin/logout')
def logout() :
	session['admin_logged_in'] = False
	session['admin_username'] = ''
	session['admin_userId'] = None
	error = None
	message = 'You are succesfully logged out!'		
	return render_template('admin.html',error=error,message=message)


@admin_views.route('/admin/contest',methods=['POST','GET'])
def addcontest():
	if request.method == 'POST' :
		db = get_db()
		#Contest Table Entries 
		date_string = request.form['start-date'] + ' ' +request.form['start-time']
		format = '%Y-%m-%d %H:%M'
		start_time = datetime.strptime(date_string, format)
		date_string = request.form['end-date'] + ' ' +request.form['end-time']
		end_time = datetime.strptime(date_string, format)
		name = request.form['contestname']
		company = admin_user(session['admin_userId'])['organization']
		shortdesc = request.form['shortdesc']
		longdesc = request.form['longdesc']
		owner = session['admin_userId']
		result=db.execute('INSERT into contest (start_time , end_time, name, company, short_description, long_description, owner) VALUES (?, ?, ?, ?, ?, ?, ?)',[start_time, end_time, name, company, shortdesc, longdesc, owner])
		#Question Table Entries 
		number_question = int(request.form['count'])
		print "Number of Questions : " +str(number_question)
		for i in range(1,number_question+1) :
			cur = db.execute('SELECT * FROM contest WHERE name=?',[name])
			cur = cur.fetchone()
			contest_id = cur['contest_id']		
			question_name = request.form['question_name'+str(i)]			
			question_desc = request.form['question_desc'+str(i)]		
			db.execute('INSERT into contest_questions ( contest_id, owner, question_name, question_string ) VALUES (?, ?, ?, ?)',[contest_id, owner, question_name, question_desc])
			number_testcase = int(request.form['count'+str(i)])
			print "	Number of Testcase : " +str(number_testcase)
			for j in range(1,number_testcase+1) :
				cur = db.execute('SELECT * FROM contest_questions WHERE question_name=?',[question_name])
				cur = cur.fetchone()
				question_id = cur['question_id']
				test = request.form['question'+str(i)+'_incase'+str(j)]
				answer = request.form['question'+str(i)+'_outcase'+str(j)]
				points = request.form['question'+str(i)+'_points'+str(j)]
				time_limit = request.form['question'+str(i)+'_tl'+str(j)]
				space_limit = request.form['question'+str(i)+'_sl'+str(j)]
				db.execute('INSERT into question_testcase ( question_id, test, answer, points, time_limit, space_limit ) VALUES (?, ?, ?, ?, ?, ?)',[question_id, test, answer, points, time_limit, space_limit])
		db.commit()
		message = "Congratulations "+" Your contest "+request.form['contestname']+" has been added "
		return render_template('admin.html' , message=message )
	return render_template('organize.html')

@admin_views.route('/admin/contests',methods=['POST','GET'])
def contest_view() :
    db = get_db()
    cur = db.execute('select * from contest where owner=?',[session['admin_userId']])
    contest_list = cur.fetchall()
    return render_template('edit_contest.html', contests=contest_list)

@admin_views.route('/admin/contest/edit/<contest_id>',methods=['POST','GET'])
def contest_details(contest_id):
    db = get_db()
    if request.method == 'POST' :
    	db.execute('update contest set name=?, company=? ,start_time=? , end_time=? , short_description = ?, long_description = ?  where contest_id=?',[request.form['contestname'], request.form['company'],request.form['start-time'],request.form['end-time'],request.form['shortdesc'],request.form['longdesc'],request.form['contestno']])
    	cur = db.execute('select * from contest where contest_id=?',request.form['contestno'])
    	contest = cur.fetchone()
    	cur = db.execute('select * from contest_questions where contest_id=?',[contest_id])
    	questions = cur.fetchall()
    	db.commit()
    	message = request.form['contestname'] + " Updated Succesfully :)"
    	return render_template('edit_contest_details.html',message=message, contest=contest , questions = questions)
    cur = db.execute('select * from contest where contest_id=?',[contest_id])
    contest = cur.fetchone()
    cur = db.execute('select * from contest_questions where contest_id=?',[contest_id])
    questions = cur.fetchall()
    return render_template('edit_contest_details.html', contest=contest, questions = questions)

@admin_views.route('/admin/question/edit/<question_id>',methods=['POST'])
def question_details(question_id):
    db = get_db()
    db.execute('update contest_questions set question_name=?, question_string=? where question_id=?',[request.form['question_name'], request.form['question_desc'],request.form['question_id']])
    cur = db.execute('select * from contest_questions where question_id=?',request.form['question_id'])
    contest = cur.fetchone()
    cur = db.execute('select * from contest_questions where contest_id=?',[contest['contest_id']])
    questions = cur.fetchall()
    message = request.form['question_name'] + " Updated Succesfully :)"
    db.commit()
    return render_template('edit_contest_details.html',message=message, contest=contest , questions = questions )
def admin_user(admin_id):
	db = get_db()
	cur = db.execute('select * from admins where admin_id=?',[admin_id])
	cur = cur.fetchone()
	return cur
