from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Bill, Responses
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
    userId = request.args.get('user')
    if not userId:
        bills = Bill.query.filter_by(status='Опубликовано')
    else:
        user = User.query.filter_by(id=userId).first()
        if (user):
            bills = filter(lambda t: t.status != 'Удалено' ,user.bills)
        else:
            abort(404)

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
def task_page(id=0):
    minimalPage = False
    billsIds = list(map(lambda t: int(t.id), current_user.bills))
    hasId = int(id) in billsIds
    if current_user.activity == 'Студент' or not hasId and id != 0:
        minimalPage = True
    
    minDate = datetime.date.today().strftime('%Y-%m-%d')
    maxDate = addMonth(datetime.date.today(), 2).strftime('%Y-%m-%d')
    if id == 0:
        if minimalPage and current_user.activity == 'Студент':
            abort(403)
        task = Bill()
        emptyTaskData = {'id': 0, 'date': minDate, 'title': '', 'deadline': minDate, 'sum': 0, 'description': '', 'category': '', 'status': 'Скрыто', 'views': 0, 'city': '', 'street': '', 'house': '', }
        task.init_of_dict(emptyTaskData)
        readOnly = True
    else:
        task = Bill().query.filter_by(id=id).first()
        readOnly = False
    if not task:
        abort(404)
    elif task.status == 'Удалено':
        abort(404)
    responses = Responses.query.filter_by(bill_id = id).all()
    resp = list(map(lambda resp: resp.user_id, responses))
    users = []
    for r in resp:
        users.append(User.query.filter_by(id=r).first())

    return render_template('addTask.html',
        title='Задачи',
        minDate=minDate,
        maxDate=maxDate,
        task=task,
        users=users,
        readOnly=readOnly,
        minimalPage=minimalPage)



@app.route('/task-response', methods=['POST'])
def task_response():
    if current_user.activity != 'Студент' or not request.json :
        abort(403)

    task_id = request.json['taskId']
    res = {'status': 'error', 'message': 'Вы уже откликнулись на эту задачу'}

    if not Responses.query.filter_by(bill_id = task_id, user_id = current_user.id).first():
        resp = Responses(bill_id=task_id, user_id=current_user.id)
        res = {'status': 'done'}
        try:
            db.session.add(resp)
            db.session.commit()
        except:
            res = {'status': 'error', 'message': 'Внутренная ошибка сервера, попробуйте попозже. ©Лунтик'}

    return jsonify(res)

@app.route('/task-accept', methods=['POST'])
def task_accept():
    if not request.json :
        abort(403)

    user_id = request.json['userId']
    task_id = request.json['taskId']

    if not int(task_id) in list(map(lambda item: int(item.id), current_user.bills)):
        abort(403)

    user = User.query.filter_by(id=user_id).first()
    task = Bill.query.filter_by(id=task_id).first()
    resp = Responses.query.filter_by(bill_id=task_id, user_id=user_id).first()
    print(resp)
    if user and task:
        if task.status == 'Опубликовано':
            resp.is_tied = True
            task.status = 'Выполняется'
            print(resp)

            db.session.commit()
            res = {'status': 'done', 'message': 'Исполнитель принят!'}
        else:
            res = {'status': 'error', 'message': 'Исполнитель уже принят!'}
    else:
        res = {'status': 'error', 'message': 'такого пользователя или задачи нет'}

    return jsonify(res)