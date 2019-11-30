from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill


@app.route('/')
@app.route('/index')
def index():
    #Рендрим и возвращаем страницу
    return render_template('index.html')

@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)

@app.errorhandler(404)
def not_found(error):
    #Реднрим и возвращаем страницу "404 Not found"
    return render_template('notFind.html')

@app.route('/query')
def query():
    #Рендрим и возвращаем страницу
    return render_template('query.html')

@app.route('/user/')
@app.route('/user/<userID>')
@login_required
#Страница юзера
def userPage(userID=None):
    if userID:
        user = User.query.filter_by(id=userID).first()
    else:
        #Если id не был дан, то возвращаем на страницу авторизации
        if current_user.is_authenticated:
            user = current_user
        else: 
            return redirect(url_for('login'))
    #Рендрим и возвращаем страницу
    return render_template('userPage.html', user=user)


#Страница с задачами
@app.route('/tasks')
def tasksList():
    bills = Bill.query.all()
    #Рендрим и возвращаем страницу
    return render_template('tasks.html', tasks=bills, title='Площадка')

@app.route('/about-us')
def about_us():
    #Рендрим и возвращаем страницу
    return render_template('aboutUs.html', title='О нас')

# Роут который отдает данные текущего пользователя
@app.route('/me')
def me():
    res = {'status': 'not authenticated'}
    if current_user.is_authenticated:
        res['status'] = 'authenticated'
        keys = ['name', 'sname', 'activity', 'born', 'id', 'mail', 'phone', 'pname', 'rating']
        user_data = current_user.to_dict()
        for key in keys:
            res[key] = user_data[key]
    return jsonify(res)
