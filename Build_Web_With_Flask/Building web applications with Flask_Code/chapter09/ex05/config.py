# coding:utf-8

class Config(object):
    "Base configuration class"
    DEBUG = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ex03.db'


class Dev(Config):
    "Our dev configuration"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'