from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask
from views import contest


# create our little application :)
app = Flask(__name__)
app.register_blueprint(contest)

if __name__ == '__main__':
	app.run()

