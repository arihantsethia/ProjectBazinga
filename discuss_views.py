from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, Blueprint
from time import gmtime, strftime
<<<<<<< HEAD

=======
>>>>>>> 7843b6aad8d96e36d50dcc5f7c4ec4a275cdaf56

discuss_views = Blueprint('discuss_views',__name__)

		
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('database.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db 


@discuss_views.route('/discuss')
def show_questions():
    db = get_db()
    com = db.execute('SELECT * FROM question_discuss AS q JOIN users AS u ON q.user_id=u.user_id order by question_id desc;')
    entries = com.fetchall()
    return render_template('show_entries.html', entries=entries)


@discuss_views.route('/discuss/add', methods=['GET'])
def add_question():
    db = get_db()
    db2 = get_db()

    user_id = session['userId']

    #comment = 'Hi'
    curtime = strftime("%Y-%m-%d %H:%M:%S")
    #use this when we need to use local  time of the server
    db.execute('insert into question_discuss (user_id, question, title, time) values (?, ?, ?, ?)',
                 [user_id, request.args.get('comment'), request.args.get('title'), curtime])
    db.commit()

    que = db.execute('SELECT question_id FROM question_discuss order by question_id DESC LIMIT 1')
    q_id = que.fetchone()

    activity = 'questioned'
    url = '/discuss/show/answers/' + str(q_id[0])
    db2.execute('insert into activity_log (user_id, activity, time, url) values (?, ?, ?, ?)',
                 [user_id, activity, curtime, url])
    db2.commit()

    flash('New comment was successfully posted')
    return redirect(url_for('.show_questions'))


@discuss_views.route('/discuss/show/answers/<int:id>', methods=[ 'GET'])
def show_answers(id=0) :
    db = get_db()
    que = db.execute('SELECT * FROM question_discuss WHERE question_id = ?', [id])
    ques = que.fetchone()
    user = db.execute('SELECT * FROM users WHERE user_id = ?', [ques[1]])
    name = user.fetchone()
    ans = db.execute('SELECT * FROM answer_discuss AS q JOIN users AS u ON q.user_id=u.user_id WHERE question_id = ? order by time desc', [id])
    entries = ans.fetchall()
    return render_template('question_discuss.html', ques=ques, entries=entries, name=name)      


@discuss_views.route('/discuss/show/answers/add', methods=['GET'])
def add_answer():
    db = get_db()
    q_id = request.args.get('q_id')
    if(request.method =='GET') :
        user_id = session['userId']
        #comment = 'Hi'
        curtime = strftime("%Y-%m-%d %H:%M:%S")
        #use this when we need to use local  time of the server
        db.execute('insert into answer_discuss (user_id, answer, question_id, time) values (?, ?, ?, ?)',
                     [user_id, request.args.get('answer'), request.args.get('q_id'), curtime])
        db.commit()

        # in activity log
        activity = 'answered' + ';' + str(request.args.get('q_id'))
        url = '/discuss/show/answers/' + str(q_id)
        db.execute('insert into activity_log (user_id, activity, time, url) values (?, ?, ?, ?)',
                 [user_id, activity, curtime, url])
        db.commit()

    que = db.execute('SELECT * FROM question_discuss WHERE question_id = ?', [q_id])
    ques = que.fetchone()

    ans = db.execute('SELECT * FROM answer_discuss WHERE question_id = ? order by time desc', [q_id])
    entries = ans.fetchall()
    user = session['username']

    user = db.execute('SELECT * FROM users WHERE user_id = ?', [ques[1]])
    name = user.fetchone()
    #return render_template('question_discuss.html', ques=ques, entries=entries, user=user)
    #return render_template('question_discuss.html', ques=ques, entries=entries, name=name)
    return redirect(url_for('.show_answers' , id = q_id))
