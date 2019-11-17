from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill


@app.route('/')
@app.route('/index')
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

@app.route('/user/')
@app.route('/user/<userID>')
@login_required
def userPage(userID=None):
    if userID:
        user = User.query.filter_by(id=userID).first()
    else:
        if current_user.is_authenticated:
            user = current_user
        else: 
            return redirect(url_for('login'))
    return render_template('userPage.html', user=user)

@app.route('/tasks')
def tasksList():
    bills = Bill.query.all()
    return render_template('tasks.html', tasks=bills, title='Площадка')

@app.route('/about-us')
def about_us():
    return render_template('aboutUs.html', title='О нас')