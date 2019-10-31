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
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            obj = User.query.filter_by(id=Id).first()
            if obj:
                return jsonify(obj.to_dict())
            else: 
                res = {'status': 'По вашему запросу ничего не найдено'}
                return jsonify(res)
@app.route('/query/add', methods=['POST'])
def queryAdd():
    if request.method == 'POST':
        if not request.json:
            abort(400)
            return ''
        json = request.json
        user = User()
        user.init_of_dict(json)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            res = {'status': 'Такие данные уже существуют'}
            return jsonify(res)
        res = {'status':'Данные добавлены'}
        return jsonify(res)

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
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            if User.query.filter_by(id = user.id).first() != None:
                User.query.filter_by(id = user.id).update(user.to_dict())
                db.session.commit()
                res = {'status':'Данные обновлены'}
                return jsonify(res)
            else:
                res = {'status': 'Данные с таким id не найдены'}
                return jsonify(res)

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
            res = {'status': 'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            if User.query.filter_by(id = user.id).first() != None:
                User.query.filter_by(id = user.id).delete()
                db.session.commit()
                res = {'status': 'Вам смешно, а пацанчик то реально умер'}
                return res
            else:
                res = {'status': 'Данные с таким id не найдены'}
                return jsonify(res)

@app.route('/src/<path:path>')
def src(path):
    return send_from_directory('src', path)