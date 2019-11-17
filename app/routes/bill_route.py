from flask import render_template, flash, redirect, url_for, send_from_directory, request, jsonify, abort
from app import db, api
from app.forms import LoginForm
from app.models import User, Bill
from flask_restful import Resource, reqparse


class Bill_api(Resource):
    """
        RESTful API
    """
    def get(self, id=None):
        if id == None:
            res = []
            for bi in Bill.query.all():
                res.append(bi.to_dict())
            return jsonify(res)
        else:
            obj = Bill.query.filter_by(id=id).first()
            if obj:
                return jsonify(obj.to_dict())
            else: 
                res = {'status': 'По вашему запросу ничего не найдено'}
                return jsonify(res)

    def post(self):
        if not request.json:
            abort(400)
            return ''
        json = request.json
        bill = Bill()
        bill.init_of_dict(json)
        try:
            db.session.add(bill)
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
        bill = Bill()
        bill.init_of_dict(json)
        if not bill.id:
            res = {'status':'Не найден обязательный параметр: id'}
            return jsonify(res)
        else:
            if Bill.query.filter_by(id = bill.id).first() != None:
                Bill.query.filter_by(id = bill.id).update(bill.to_dict())
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

        query = Bill.query.filter_by(id = id)
        if query.first() != None:
            query.delete()
            db.session.commit()
            res = {'status': 'Запись удалена!'}
            return res
        else:
            res = {'status': 'Данные с таким id не найдены'}
            return jsonify(res)


api.add_resource(Bill_api, '/api/bill', '/api/bill/', '/api/bill/<id>')
