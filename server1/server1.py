# Main File : This has to be run to start the server
from __future__ import with_statement
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint, jsonify
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack
from Queue import PriorityQueue
from time import gmtime, strftime
import bw
# Database Configuration
DATABASE = '../database.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# Defining the application by creating an instance of Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def curtime():
	return strftime("%Y-%m-%d %H:%M:%S")


def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		sqlite_db = sqlite3.connect('../database.db')
		sqlite_db.row_factory = sqlite3.Row
		top.sqlite_db = sqlite_db
	return top.sqlite_db 

@app.route('/', methods=['GET', 'POST'])
def evalreq():
	g.params = request
	return render_template('index.html')

@app.after_request
def evaluate(response):
	db = get_db()
	request = g.params
	if request.method=='POST':
		print request.form
		userid = request.form['user_id']
		code = request.form['code']
		lang = request.form['lang']
		id = request.form['qid']

		db.execute('insert into submissions (user_id, submission_time, code, lang, points, question_id) VALUES (?,?,?,?,?,?)', [userid, curtime(), code, lang, 0, id])
		cur = db.execute('SELECT last_insert_rowid() AS id FROM submissions');
		sid = int(cur.fetchone()['id'])

		cur = db.execute('select username from users where user_id = ?', [userid])
		username = cur.fetchone()['username']
		cur = db.execute('select question_name from contest_questions where question_id = ?', [id])
		qname = cur.fetchone()['question_name']
		activity_string = '%s solved %s' % (username, qname)
		url = 'http://localhost:5000/questions/%d' % int(id)

		cur = db.execute('SELECT * FROM question_testcase WHERE question_id = ?', [id])
		testcases = cur.fetchall()
		pts = 0
		for tc in testcases:
			(out, err) = bw.compilerun(sid, code, tc['test'], lang, tc['space_limit'], tc['time_limit'])
			print 'ERROR: %s' % err
			#result type: -1 => WRONG ANSWER, -2 => ERROR, >0 => correct, -3 => TLE
			if (err == '' and out == tc['answer']):
				pts += int(tc['points'])
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,"",0,0)', [tc['testcase_id'], sid, tc['points']])
			elif (err[:3] == 'TLE'):
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,?,0,0)', [tc['testcase_id'], sid, -3, err])
			elif (err != ''):
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,?,0,0)', [tc['testcase_id'], sid, -2, err])
			elif (out != tc['answer']):
				db.execute('insert into submission_testcase (testcase_id, submission_id, result_type, result, run_time, run_space) VALUES (?,?,?,?,0,0)', [tc['testcase_id'], sid, -1, ""])
		db.execute('UPDATE submissions SET points = ? WHERE id=?', [pts, sid])
		#return render_template('submission_result.html', points=pts)
		#add to activity log
		if pts > 0:
			db.execute('insert into activity_log (user_id, activity, time, url) VALUES (?,?,?,?)', [userid, activity_string, curtime(), url])
		db.commit()
		print 'points: %d' % pts
		return response
		#return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True, port=2345)
	

