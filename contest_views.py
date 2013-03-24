from flask import Flask, render_template, redirect, url_for, Blueprint

contest_views = Blueprint('contest_views',__name__)

@contest_views.route('/practice')
def index():
    return render_template("practice.html")

@contest_views.route('/compete')
def contest():
    return render_template("compete.html")