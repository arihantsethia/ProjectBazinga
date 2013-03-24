from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack,Blueprint

DATABASE = '/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

'''
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
		print db'''

def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect('flaskr.db')
        print sqlite_db
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

db = None
db =get_db()