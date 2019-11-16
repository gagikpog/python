from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)

@app.errorhandler(404)
def not_found(error):
    return render_template('notFind.html')

@app.route('/query')
def query():
    return render_template('query.html')