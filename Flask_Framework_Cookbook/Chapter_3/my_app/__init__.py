from flask import Flask
from flask.ext.mongoengine import MongoEngine
from redis import Redis


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'my_catalog'}
app.debug = True
db = MongoEngine(app)

redis = Redis()

from Flask_Framework_Cookbook.Chapter_10.my_app import catalog
app.register_blueprint(catalog)
