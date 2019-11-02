from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import app, db
from app.forms import LoginForm
from app.models import User, Bill


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)