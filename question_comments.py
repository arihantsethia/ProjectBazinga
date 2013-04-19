from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime
from login_views import user


question_comments = Blueprint('question_comments',__name__)


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('database.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db 



@question_comments.route('/')
def show_questions():
    return 'Welcome you should not come here'


@question_comments.route('/show/comments/<int:id>', methods=['POST' , 'GET'])
def show_question_comments(id=0):
    print 'in db'
    db = get_db()  
#    q_no = request.form['q_no']       
    cur = db.execute('SELECT * FROM question_comments WHERE question_id = ? order by time DESC', [id])
    com = cur.fetchall()
    users =[]
    for i in range(len(com)) :
        users.append(user(com[i]['user_id'])['username'])
    
    return render_template("question_comments.html", entries=com , q_no=id, users=users)
    #return render_template("discussion_forum.html")


@question_comments.route('/add_comments', methods=['GET'])
def add_question_comment():
    db = get_db()
    user_id = session['userId']
    q_no = request.args.get('q_id')
    print q_no
    curtime = strftime("%Y-%m-%d %H:%M:%S")
    if(request.method =='GET') :
        db.execute('insert into question_comments (user_id, comment, question_id, time) values (?, ?, ?, ?)',
                     [user_id, request.args.get('comment'), q_no, curtime])
        db.commit()  
        print "Here F"
        activity = 'commented' + ';' + str(q_no)
        url = '/show/comments/' + str(q_no)
        db.execute('insert into activity_log (user_id, activity, time, url) values (?, ?, ?, ?)',
                     [user_id, activity, curtime, url])
        db.commit()
    cur = db.execute('SELECT * FROM question_comments WHERE question_id = ? order by comment_id ', [q_no])
    com = cur.fetchall()
    db2 = get_db()
    cur2 = db2.execute('select * from contest_questions where question_id = ?', [q_no])
    q = cur2.fetchone()
    return redirect(url_for('contest_views.show_question' , id = q_no))
