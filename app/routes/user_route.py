from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import db, api
from app.forms import LoginForm
from app.models import User, Bill
from flask_restful import Resource, reqparse
from flask_login import current_user

class User_api(Resource):
    """
        RESTful API
    """
    #Запрос на получение юзера
    def get(self, id=None):
        if id == None:
            #Если id не был дан, то возвращаем ошибку
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            #Если дан id, то находим юзера с таким id
            obj = User.query.filter_by(id=id).first()
            if obj:
                #Если юзер с таким id найден, то возвращаем
                return jsonify(obj.to_dict())
            else:
                #Иначе, возвращаем ошибку
                res = {'status': 'По вашему запросу ничего не найдено'}
                return jsonify(res)

    #Запрос на добавление нового юзера
    def post(self, id=None):
        #Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
            return ''
        json = request.json
        #Создаем новый объект
        user = User()
        user.init_of_dict(json)
        try:
            #Пытаемся добавить полученные данные в БД
            db.session.add(user)
            db.session.commit()
        except:
            #Если не получилось, то возвращаем ошибку
            res = {'status': 'Такие данные уже существуют'}
            return jsonify(res)
        res = {'status':'Данные добавлены'}
        return jsonify(res)

    #Запрос на обновление данных юзера
    def put(self, id=None):
        #Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
            return ''
        json = request.json
        #Создаем новый объект
        user = User()
        user.init_of_dict(json)
        if not user.id:
            #Если id не был дан, то возвращаем ошибку
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            #Находим юзера и обновляем данные
            if not user.id == current_user.id:
                res = {'status':'Попытка поменять чужие данные'}
                return jsonify(res)
            if User.query.filter_by(id = user.id).first() != None:
                User.query.filter_by(id = user.id).update(user.to_dict())
                db.session.commit()
                res = {'status':'Данные обновлены'}
                return jsonify(res)
            else:
                #Если юзер не найден, то возвращаем ошибку
                res = {'status': 'Данные с таким id не найдены'}
                return jsonify(res)

    #Запрос на удаление юзера
    def delete(self, id=None):
        if id == None:
            #Если id не был дан, то возвращаем ошибку
            res = {'status': 'Не найден обязательный параметр: id'}
            return jsonify(res)

        query = User.query.filter_by(id = id)
        if query.first() != None:
            #Находим юзера и удаляем его
            query.delete()
            db.session.commit()
            res = {'status': 'Вам смешно, а пацанчик то реально умер'}
            return res
        else:
            #Если юзер не найден, то возвращаем ошибку
            res = {'status': 'Данные с таким id не найдены'}
            return jsonify(res)


api.add_resource(User_api, '/api/user', '/api/user/', '/api/user/<id>')
