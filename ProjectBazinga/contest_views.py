from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime

contest_views = Blueprint('contest_views',__name__)
#curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #use this when we need to use the GMT
curtime = strftime("%Y-%m-%d %H:%M:%S") #use this when we need to use local  time of the server


#This function sets the database connection
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('flaskr.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

@contest_views.route('/practice')
def index():
    return render_template("practice.html")

@contest_views.route('/contests')
def contests():
	db = get_db()
	cur = db.execute('SELECT * FROM contest WHERE end_time > ?',[curtime])
	cs = cur.fetchall()
	return render_template("contests.html", contests=cs)

@contest_views.route('/contests/<int:contest_id>')
def show_contest(contest_id=0):
	db = get_db()
	cur = db.execute('SELECT * FROM contest_questions WHERE contest_id = ?', [contest_id])
	qs = cur.fetchall()
	return render_template("contest_questions.html", questions=qs)

@contest_views.route('/contests/question/<int:id>', methods=['GET','POST'])
def show_question(id=0):
	if(request.method =='POST') :
		f_name = 'asdf'+curtime+'.txt'
		fo = open('uploads/'+f_name, "wb")
		fo.write( "Python is a great language.\nYeah its great!!\n");
	db = get_db()
	cur = db.execute('select * from contest_questions where question_id = ?', [id])
	q = cur.fetchone()
	cur = db.execute('select * from contest where contest_id = ?', [q['contest_id']])
	c = cur.fetchone()
	return render_template("show_question.html", question=q, contest=c)
	

