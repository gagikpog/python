from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from config import Config
from flask_script import Manager
from flask_login import LoginManager
from flask_admin import Admin
#from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore #Хранилище данных SQLAlchemy
from flask_security import Security
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager=Manager(app)
manager.add_command('db',MigrateCommand)
login = LoginManager(app)
login.login_view = 'login'
#login.login_view = 'login'
from app import models
from app.routes import user_route, routes, bill_route, auth_route
#администрирование- продумать позже
### ADMIN ###
#from models import *
#admin = Admin(app)
#admin.add_view(ModelView())

### Flask-security ###
#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
#security = Security(app, user_datastore)
