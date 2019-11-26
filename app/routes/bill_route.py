from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import db, api
from app.forms import LoginForm
from app.models import User, Bill
from flask_restful import Resource, reqparse


class Bill_api(Resource):
    """
        RESTful API
    """
    
    #Запрос на получение задач
    def get(self, id=None):
        #Если id не был дан, то возвращаем все задачи
        if id == None:
            res = []
            for bi in Bill.query.all():
                #Добавляем все задачи в list
                res.append(bi.to_dict())
            #Возвращаем json с задачами
            return jsonify(res)
        else:
            #Если дан id, то находим задачу с таким id
            obj = Bill.query.filter_by(id=id).first()
            if obj:
                #Если задача с таким id найдена, то возвращаем
                return jsonify(obj.to_dict())
            else: 
                #Иначе, возвращаем ошибку
                res = {'status': 'По вашему запросу ничего не найдено'}
                return jsonify(res)


    #Запрос на добавление новой задачи
    def post(self):
        #Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
            return ''
        json = request.json
        #Создаем новый объект
        bill = Bill()
        bill.init_of_dict(json)
        try:
            #Пытаемся добавить полученные данные в БД
            db.session.add(bill)
            db.session.commit()
        except:
            #Если не получилось, то возвращаем ошибку
            res = {'status': 'Такие данные уже существуют'}
            return jsonify(res)
        res = {'status':'Данные добавлены'}
        return jsonify(res)

    #Запрос на обновление данных
    def put(self, id=None):
        #Если запрос неправильный, то возвращаем 400 Bad Request
        if not request.json:
            abort(400)
            return ''
        json = request.json
        #Создаем новый объект
        bill = Bill()
        bill.init_of_dict(json)        
        if not bill.id:
            #Если id не был дан, то возвращаем ошибку
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            #Находим задачу и обновляем данные
            if Bill.query.filter_by(id = bill.id).first() != None:
                Bill.query.filter_by(id = bill.id).update(bill.to_dict())
                db.session.commit()
                res = {'status':'Данные обновлены'}
                return jsonify(res)
            else:
                #Если задача не найдена, то возвращаем ошибку
                res = {'status': 'Данные с таким id не найдены'}
                return jsonify(res)


    #Запрос на удаление задачи
    def delete(self, id=None):
        if id == None:
            #Если id не был дан, то возвращаем ошибку
            res = {'status': 'Не найден обязательный параметр: id'}
            return jsonify(res)

        query = Bill.query.filter_by(id = id)
        if query.first() != None:
            #Находим задачу и удаляем её
            query.delete()
            db.session.commit()
            res = {'status': 'Запись удалена!'}
            return res
        else:
            #Если задача не найдена, то возвращаем ошибку
            res = {'status': 'Данные с таким id не найдены'}
            return jsonify(res)


api.add_resource(Bill_api, '/api/bill', '/api/bill/', '/api/bill/<id>')
