from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, _app_ctx_stack
from views import views
from contest_views import contest_views

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.register_blueprint(views)
app.register_blueprint(contest_views)

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
		print db

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

if __name__ == '__main__':
	#init_db()
	app.run(debug=True)
	

