from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime


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
    cur = db.execute('SELECT * FROM question_comments WHERE question_id = ? order by comment_id', [id])
    com = cur.fetchall()

    #print 'in db2'
    db2 = get_db()
    #print 'after get_db2 '
    cur2 = db2.execute('select * from contest_questions where question_id = ?', [id])
    #print 'afetr execute statement'
    q = cur2.fetchone()
    #print 'afetr fetchone'
    
    return render_template("question_comments.html", entries=com , q_no=id, question=q)
    #return render_template("discussion_forum.html")


@question_comments.route('/add_comments', methods=['GET'])
def add_question_comment():
    db = get_db()
    user_id = session['userId']

    q_no = request.args.get('q_id')
    curtime = strftime("%Y-%m-%d %H:%M:%S")
    if(request.method =='GET') :
    #use this when we need to use local  time of the server
        db.execute('insert into question_comments (user_id, comment, question_id, time) values (?, ?, ?, ?)',
                     [user_id, request.args.get('comment'), q_no, curtime])
        db.commit()

        
        # in to activity log
        activity = 'commented' + ';' + str(q_no)
        url = '/show/comments/' + str(q_no)
        db.execute('insert into activity_log (user_id, activity, time, url) values (?, ?, ?, ?)',
                     [user_id, activity, curtime, url])
        db.commit()

        flash ('New comment was successfully posted')



    cur = db.execute('SELECT * FROM question_comments WHERE question_id = ? order by comment_id ', [q_no])
    com = cur.fetchall()

    db2 = get_db()
    #print 'after get_db2 '
    cur2 = db2.execute('select * from contest_questions where question_id = ?', [q_no])
    #print 'afetr execute statement'
    q = cur2.fetchone()
    #print 'afetr fetchone'
    
    #return render_template("question_comments.html", entries=com , q_no=q_no , question=q)
    return redirect(url_for('.show_question_comments' , id = q_no))