from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db, login_manager
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill
from wtforms.validators import ValidationError

#Авторизация

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if '@' in username:
            user = User.query.filter_by(mail=username).first()
        else:
            user = User.query.filter_by(phone=username).first()
        login_user(user)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    return render_template('login.html',  title='Вход', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        userData = {
            'name': form.name.data,
            'pname': form.pname.data,
            'sname': form.sname.data,
            'activity': form.activity.data
        }
        uname = form.username.data
        user = None
        if '@' in uname:
            userData["mail"] = uname
        else:
            userData["phone"] = uname

        user = User()
        user.init_of_dict(userData)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Ok!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form) 

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()