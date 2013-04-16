# profile_views.py : Handles the views for Profile Module

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime
import bw

profile_views = Blueprint('profile_views',__name__)

#This function sets the database connection
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('database.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db 

@profile_views.route('/follow_unfollow/<followingid>/<action>')
def follow_unfollow(followingid,action):
	db = get_db()
	if int(action):
		cur = db.execute('insert into follow (follower,following) values (?,?)',[int(session['userId']),int(followingid)])
	else:
		cur = db.execute('delete from follow where follower=? and following=?',[int(session['userId']),int(followingid)])
	string = '/profile/'+str(followingid)
	db.commit()
	return redirect(string)

#127.0.0.1:5000/profile/<number> shows the profile of the person with uid=<number>
@profile_views.route('/profile/<path>')
def profile(path):
    db = get_db()
    cur = db.execute('select * from users where user_id=?',[path])
    user = cur.fetchone()
    cur = db.execute('select * from follow where follower=? and following=?',[session['userId'],path])
    check=cur.fetchall()
    if int(path)==session['userId']:
	   flag=1     #1 - same user profile, 0-diff user and following, 2-diff user and not following
    elif check:
	   flag=0
    else:
	   flag=2
    return render_template('profile.html', user=user, flag=flag)

#profile edit page - you can edit your profile
@profile_views.route('/profile/edit')
def profile_edit():
    db = get_db()
    cur = db.execute('select * from users where user_id=?',[session['userId']])
    user = cur.fetchone()
    return render_template('profile_edit.html', user=user)


#intermediary buffer page - while the edit changes are being saved, this redirects to profile page
@profile_views.route('/profile/editing',methods=['POST'])
def editing():
    db = get_db()
    db.execute('update users set name=?, age=? where user_id=?',[request.form['name'], request.form['age'],session['userId']])
    db.commit()
    string = '/profile/'+str(session['userId'])
    return redirect(string)

#shows you all the followers and their correct submissions
@profile_views.route('/profile/follow')
def follow():
	db = get_db();
	cur = db.execute('select following from follow where follower=?',[session['userId']])
	following = cur.fetchall()
  	info = []
	for temp in following:
		db = get_db()
		cur = db.execute('select * from history where status=? and user_id=? order by rowid desc',['Accepted',temp[0]])
		info = info + cur.fetchall()		
	return render_template('follow.html',following=following,info=info)