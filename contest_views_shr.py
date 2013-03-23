from flask import Flask, render_template, redirect, url_for, Blueprint
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
contest_views = Blueprint('contest_views',__name__)

