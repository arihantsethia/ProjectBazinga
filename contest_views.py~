from flask import Flask, render_template, redirect, url_for, Blueprint
import contest_p
import db from runserver
contest_views = Blueprint('contest_views',__name__)

@contest_views.route('/contests')
def contest_list():
    
    #fetch current online contest from table contest
    cur = db.execute('select time(end_time), from contest where time(current_timestamp, 'localtime') < time(end_time)')
    contests_live=cur.fetchall();
    #send live contest names to browser
    return render_template("contests.html",contests=contests_live)

if __name__ == '__main__':
    contest_views.run(Debug)
