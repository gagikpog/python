import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'studer.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    JSON_AS_ASCII = False

    SECURITY_PASSWORD_SALT = 'super hash'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
