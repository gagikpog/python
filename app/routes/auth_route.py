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
    loginForm = LoginForm()
    registrForm = RegistrationForm()
    submit_mode = registrForm.submit.raw_data and registrForm.submit.raw_data[0]

    if submit_mode == 'Войти' and loginForm.validate_on_submit():
        username = loginForm.username.data
        if '@' in username:
            user = User.query.filter_by(mail=username).first()
        else:
            user = User.query.filter_by(phone=username).first()
        login_user(user)
        flash('Login requested for user {}, remember_me={}'.format(
            loginForm.username.data, loginForm.remember_me.data))
        
        next = request.args.get('next')
        return redirect(next or url_for('index'))

    if submit_mode == 'Регистрация' and registrForm.validate_on_submit():
        userData = {
            'name': registrForm.name.data,
            'pname': registrForm.pname.data,
            'sname': registrForm.sname.data,
            'activity': registrForm.activity.data
        }
        uname = registrForm.username.data
        user = None
        if '@' in uname:
            userData["mail"] = uname
        else:
            userData["phone"] = uname

        user = User()
        user.init_of_dict(userData)

        user.set_password(registrForm.password.data)
        db.session.add(user)
        db.session.commit()
        next = request.args.get('next')
        login_user(user)
        return redirect(next or url_for('index'))

    return render_template('login.html',  title='Вход', loginForm=loginForm, registrForm=registrForm)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()