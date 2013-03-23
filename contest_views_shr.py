from flask import Flask, render_template, redirect, url_for, Blueprint
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

import db from 
contest_views = Blueprint('contest_views',__name__)

@contest_views.route('/contests/<int:contest_id>')
def show_contest(contest_id=0):
	cur = db.execute('select * from contest_questions where contest_id = ?', contest_id)
	qs = cur.fetchall()
	return render_template("contest_questions.html", questions=qs)

@contest_views.route('/questions/<int:id>')
def show_question(id=0):
	cur = db.execute('select * from contest_questions where question_id = ?', id)
	q = cur.fetchone()
	cur = db.execute('select * from contest where contest_id = ?', qs.contest_id)
	c = cur.fetchone()
	return render_template("show_question.html", question=q, contest=c)