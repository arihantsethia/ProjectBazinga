from flask import Flask, render_template, redirect, url_for, Blueprint

contest = Blueprint('contest',__name__)

@contest.route('/')
def index():
    return render_template("index.html")

