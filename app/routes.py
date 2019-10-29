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

@app.route('/query/read', methods=['GET'])
def queryRead():
    if request.method == 'GET':
        Id = request.args.get('id')
        if not Id:
            return "Не найден обязательный параметр: id"
        else:
            user = User.query.filter_by(id=Id).first()
            if user:
                return jsonify(user.to_dict())
            else: 
                return 'По вашему запросу ничего не найдено'
@app.route('/query/create', methods=['GET'])
def queryCreate():
    if request.method == 'GET':
        db.create_all()
        return "База создана"
@app.route('/query/add', methods=['POST'])
def queryAdd():
    if request.method == 'POST':
        if not request.json:
            abort(400)
            return ''
        json = request.json
        user = User()
        user.init_of_dict(json)
        if User.query.filter_by(mail = user.mail).first() != None:
            return "Такая почта уже добавлена"
        if User.query.filter_by(phone = user.phone).first() != None:
            return "Такой номер уже добавлен"
        db.session.add(user)
        db.session.commit()
        res = "Данные добавлены"
        return res

@app.route('/query/update', methods=['POST'])
def queryUpdate():
    if request.method == 'POST':
        if not request.json:
            abort(400)
            return ''
        json = request.json
        user = User()
        user.init_of_dict(json)
        if not user.id:
            return "Не найден обязательный параметр: id"
        else:
            if User.query.filter_by(id = user.id).first() != None:
                User.query.filter_by(id = user.id).update(user.to_dict())
                db.session.commit()
                res = "Данные обновлены"
                return res
            else:
                return "Данные с таким id не найдены"

@app.route('/query/delete', methods=['POST'])
def queryDelete():
    if request.method == 'POST':
        if not request.json:
            abort(400)
            return ''
        json = request.json
        user = User()
        user.init_of_dict(json)
        if not user.id:
            return "Не найден обязательный параметр: id"
        else:
            if User.query.filter_by(id = user.id).first() != None:
                User.query.filter_by(id = user.id).delete()
                db.session.commit()
                res = "Вам смешно, а пацанчик то реально умер"
                return res
            else:
                return "Данные с таким id не найдены"

@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)