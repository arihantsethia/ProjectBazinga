# Profile Module
# Incharge 						: Siddharth Ancha
# Features Handled by this module : Profile Display
# 								  Profile Edit
# 								  Follow/Unfollow
# 								  Diplay followees and thier info
# 								  Notifications
# 								  User search


from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint
from time import gmtime, strftime
<<<<<<< HEAD

=======
>>>>>>> 7843b6aad8d96e36d50dcc5f7c4ec4a275cdaf56

profile_views = Blueprint('profile_views',__name__)

#This function sets the database connection
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('database.db')
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db 

@profile_views.route('/notifications')		# Handles Notifications  - Notifications button in Header Toolbar
def notifications():
	db = get_db()
	cur = db.execute('select activity_log.user_id, activity, url, time, username, following from activity_log inner join (follow inner join users on following=users.user_id) on activity_log.user_id=following where follower=?',[session['userId']])
	activities = cur.fetchall()
	length = len(activities)
	return render_template('notifications.html', activities=activities, length=length)

@profile_views.route('/follow_unfollow/<followingid>/<action>')
def follow_unfollow(followingid,action):	#Provides buttons and actions for Follow and Unfollow
	db = get_db()
	if int(action):
		cur = db.execute('insert into follow (follower,following) values (?,?)',[session['userId'], followingid ])
	else:
		cur = db.execute('delete from follow where follower=? and following=?',[session['userId'],int(followingid)])
	db.commit()
	string = '/profile/'+str(followingid)
	return redirect(string)



#127.0.0.1:5000/profile/<number> shows the profile of the person with uid=<number>
@profile_views.route('/profile/<path>')		#To display profile. Inputs id of user and renders profile page of that particular user
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
@profile_views.route('/profile/edit')		#To edit user profile
def profile_edit():
    db = get_db()
    cur = db.execute('select * from users where user_id=?',[session['userId']])
    user = cur.fetchone()
    return render_template('profile_edit.html', user=user)


#intermediary buffer page - while the edit changes are being saved, this redirects to profile page
@profile_views.route('/profile/editing',methods=['POST'])	#intermediary stage of editing in user profile edit
def editing():
    db = get_db()
    db.execute('update users set username=?, name=?, email=?, contact=?, website=?, profession=?, organization=?, resume=?, picture=? where user_id=?',[request.form['username'], request.form['name'],request.form['email'],request.form['contact'],request.form['website'],request.form['profession'],request.form['organization'],request.form['resume'],request.form['picture'],session['userId']])
    db.commit()
    string = '/profile/'+str(session['userId'])
    return redirect(string)

#shows you all the followers and their correct submissions
@profile_views.route('/profile/follow/<path>')		# to display the users being followed and all their solved/partially solved problems
def follow(path):
	db = get_db()
	if int(path)==-1:
		cur = db.execute('select follow.following, users.username, users.name from follow inner join users on follow.following=users.user_id where follow.follower=?',[session['userId']])
	else:
		cur = db.execute('select follow.following, users.username, users.name from follow inner join users on follow.following=users.user_id where follow.follower=? and follow.following=?',[session['userId'],int(path)])
	following = cur.fetchall()
	info = []
	for temp in following:
		db = get_db()
		cur = db.execute('select * from submissions inner join contest_questions on submissions.question_id=contest_questions.question_id where user_id=? and points>0',[temp[0]])
		#cur = db.execute('select * from submissions where user_id=? order by submission_time desc',[temp[0]])
		info = info + cur.fetchall()
	return render_template('follow.html',following=following,info=info)
	
@profile_views.route('/search')
def search():			#Implements the 'LIKE' search feature of SQL on user-names to find and befriend users
	name = request.args.get("search")
	db = get_db()
	cur = db.execute('select * from users where name LIKE ?',['%'+name+'%'])
	names = cur.fetchall()
	count = len(names)
	return render_template('search_results.html',names=names, count=count)
