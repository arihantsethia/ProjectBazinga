from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, Blueprint
from time import gmtime, strftime
import bw

discuss_views = Blueprint('discuss_views',__name__)

		
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('comments.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db 



@discuss_views.route('/discuss')
def show_questions():
    db = get_db()
    com = db.execute('SELECT * FROM question_discuss order by question_id desc;')
    entries = com.fetchall()
    return render_template('show_entries.html', entries=entries)


@discuss_views.route('/discuss/add', methods=['POST'])
def add_question():
    db = get_db()

    user_id = 1

    #comment = 'Hi'
    curtime = strftime("%Y-%m-%d %H:%M:%S")
    #use this when we need to use local  time of the server
    db.execute('insert into question_discuss (user_id, question, time) values (?, ?, ?)',
                 [user_id, request.form['comment'], curtime])
    db.commit()

    activity = 'questioned'
    db.execute('insert into activity_log (user_id, activity, time) values (?, ?, ?)',
                 [user_id, activity, curtime])
    db.commit()

    flash('New comment was successfully posted')
    return redirect(url_for('.show_questions'))


@discuss_views.route('/discuss/show/answers', methods=['POST'])
def show_answers():
    db = get_db()
    q_id = request.form['q_id']

    """
        this need to be checked 
    que1 = db.execute('SELECT * FROM question_discuss WHERE question_id = ?', [q_id])
    question = que1.fetchone()
    time = question.time
    """

    que2 = db.execute('SELECT * FROM question_discuss WHERE question_id >  ? order by question_id desc', [q_id])
    preques = que2.fetchall()

    que = db.execute('SELECT * FROM question_discuss WHERE question_id = ?', [q_id])
    ques = que.fetchone()

    ans = db.execute('SELECT * FROM answer_discuss WHERE question_id = ? order by time desc', [q_id])
    entries = ans.fetchall()

    que3 = db.execute('SELECT * FROM question_discuss WHERE question_id < ? order by question_id desc ', [q_id])
    postques = que3.fetchall()
    return render_template('show_entries_with.html', preques=preques, ques=ques, postques=postques, entries=entries)


@discuss_views.route('/discuss/show/answers/add', methods=['POST'])
def add_answer():
    db = get_db()
    if(request.method =='POST') :
        user_id = 1
        #comment = 'Hi'
        curtime = strftime("%Y-%m-%d %H:%M:%S")
        #use this when we need to use local  time of the server
        db.execute('insert into answer_discuss (user_id, answer, question_id, time) values (?, ?, ?, ?)',
                     [user_id, request.form['answer'], request.form['q_id'], curtime])
        db.commit()

        # in activity log
        activity = 'answered' + ';' + str(request.form['q_id'])
        db.execute('insert into activity_log (user_id, activity, time) values (?, ?, ?)',
                     [user_id, activity, curtime])
        db.commit()
        flash('New answer was successfully posted')

    q_id = request.form['q_id']    
    que2 = db.execute('SELECT * FROM question_discuss WHERE question_id > ? order by question_id desc ', [q_id])
    preques = que2.fetchall()

    que = db.execute('SELECT * FROM question_discuss WHERE question_id = ?', [q_id])
    ques = que.fetchone()

    ans = db.execute('SELECT * FROM answer_discuss WHERE question_id = ? order by time desc', [q_id])
    entries = ans.fetchall()

    que3 = db.execute('SELECT * FROM question_discuss WHERE question_id < ? order by question_id desc', [q_id])
    postques = que3.fetchall()
    return render_template('show_entries_with.html', preques=preques, ques=ques, postques=postques, entries=entries)
