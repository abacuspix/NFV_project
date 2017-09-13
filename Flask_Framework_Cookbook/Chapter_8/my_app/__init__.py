from flask import Flask
from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from Flask_Framework_Cookbook.Chapter_10 import my_app as views

admin = Admin(app, index_view=views.MyAdminIndexView())
admin.add_view(views.HelloView(name='Hello'))
admin.add_view(views.UserAdminView(views.User, db.session))

from Flask_Framework_Cookbook.Chapter_10.my_app import auth
app.register_blueprint(auth)

db.create_all()
