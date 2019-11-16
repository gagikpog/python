from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import db, api
from app.forms import LoginForm
from app.models import User, Bill
from flask_restful import Resource, reqparse


class User_api(Resource):
    """
        RESTful API
    """
    def get(self, id=None):
        if id == None:
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            obj = User.query.filter_by(id=id).first()
            if obj:
                return jsonify(obj.to_dict())
            else: 
                res = {'status': 'По вашему запросу ничего не найдено'}
                return jsonify(res)

    def post(self, id=None):
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

    def put(self, id=None):
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

    def delete(self, id=None):
        if id == None:
            res = {'status': 'Не найден обязательный параметр: id'}
            return jsonify(res)

        query = User.query.filter_by(id = id)
        if query.first() != None:
            query.delete()
            db.session.commit()
            res = {'status': 'Вам смешно, а пацанчик то реально умер'}
            return res
        else:
            res = {'status': 'Данные с таким id не найдены'}
            return jsonify(res)


api.add_resource(User_api, '/api/user', '/api/user/', '/api/user/<id>')
