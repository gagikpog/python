from datetime import datetime
from app import db

class mixin():
    def to_dict(self):
        res = {}
        di = self.__dict__
        j = 0
        for i in di:
            if j == 0:
                j+=1
                continue
            res[str(i)] = getattr(self, i)
        return res

    def init_of_dict(self, _dict):
        for key, val in _dict.items():
            setattr(self, key, val)

class User(db.Model, mixin):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(32), index=True, unique=True)
    mail = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(64))
    sname = db.Column(db.String(64))
    pname = db.Column(db.String(64))
    born = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    activity = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))

    bills = db.relationship('Bill', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}, {}>'.format(self.name, self.mail)


class Bill(db.Model, mixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(64))
    deadline = db.Column(db.DateTime)
    summ = db.Column(db.Integer)
    description = db.Column(db.String(512))
    category = db.Column(db.Integer)
    status = db.Column(db.String(32))
    views = db.Column(db.Integer)

    client = db.Column(db.Integer, db.ForeignKey('user.id'))
    # student = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Bill {}>'.format(self.title)
