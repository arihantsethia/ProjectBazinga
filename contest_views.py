# contest_vies.py : Handles the views for Contest Module

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime
import bw

#Defining the Blueprint for contest_views.py
contest_views = Blueprint('contest_views',__name__)

#curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime()) #use this when we need to use the GMT
curtime = strftime("%Y-%m-%d %H:%M:%S") #use this when we need to use local  time of the server


#This function sets the database connection
def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect('database.db')
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db
	return top.sqlite_db 


@contest_views.route('/code/practice')
def index():
    return render_template("practice.html")


@contest_views.route('/code')
def contests():
	db = get_db()
	cur = db.execute('SELECT * FROM contest WHERE end_time > ?',[curtime])
	cs = cur.fetchall()
	return render_template("code.html", contests=cs)


@contest_views.route('/code/contest/<int:contest_id>')
def show_contest(contest_id=0):
	db = get_db()
	cur = db.execute('SELECT * FROM contest_questions WHERE contest_id = ?', [contest_id])
	qs = cur.fetchall()
	return render_template("contest_questions.html", questions=qs)

@contest_views.route('/code/questions/<int:id>', methods=['GET','POST'])
def show_question(id=0):
	db = get_db()

	if(request.method =='POST') :
		#f_name = 'asdf'+curtime+'.txt'
		#fo = open('uploads/'+f_name, "wb")
		#fo.write( "Python is a great language.\nYeah its great!!\n");
		code = request.form['code']
		lang = request.form['lang']

		userid = 0;

		db.execute('insert into submissions (user_id, submission_time, code, lang, points) VALUES (?,?,?,?,?)', [userid, curtime, code, lang, 0])
		cur = db.execute('SELECT last_insert_rowid() AS id FROM submissions');
		sid = int(cur.fetchone()['id'])

		cur = db.execute('SELECT * FROM question_testcase WHERE question_id = ?', [id])
		testcases = cur.fetchall()
		pts = 0
		for tc in testcases:
			(out, err) = bw.compilerun(sid, code, tc['test'], lang, tc['space_limit'], tc['time_limit'])
			if (err == '' and out == tc['answer']):
				pts += int(tc['points'])
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,"",0,0)', [tc['testcase_id'], sid, tc['points']])
			else:
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,?,0,0)', [tc['testcase_id'], sid, 0, err])
		db.execute('UPDATE submissions SET points = ? WHERE id=?', [pts, sid])
		#return render_template('submission_result.html', points=pts)
		db.commit()
		print 'points: %d' % pts


	cur = db.execute('select * from contest_questions where question_id = ?', [id])
	q = cur.fetchone()
	cur = db.execute('select * from contest where contest_id = ?', [q['contest_id']])
	c = cur.fetchone()
	return render_template("show_question.html", question=q, contest=c)
