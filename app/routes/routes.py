from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill
import datetime
from app.utility.utility import addMonth


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
    return render_template('notFound.html')

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

@app.route('/task-page/<id>')
@app.route('/task-page/')
@app.route('/task-page')
@login_required
def task_page(id=None):
    if current_user.activity == 'Студент':
        abort(403)
    minDate = datetime.date.today().strftime('%Y-%m-%d')
    maxDate = addMonth(datetime.date.today(), 2).strftime('%Y-%m-%d')
    if id == None:
        task = Bill()
        readOnly = True
    else:
        task = Bill().query.filter_by(id=id).first()
        readOnly = False
    if not task:
        abort(404)
    return render_template('addTask.html', title='Задачи', minDate=minDate, maxDate=maxDate, task=task, readOnly=readOnly)
