from flask import Flask
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

api = Api(app)

from Flask_Framework_Cookbook.Chapter_10.my_app import catalog
app.register_blueprint(catalog)

db.create_all()
