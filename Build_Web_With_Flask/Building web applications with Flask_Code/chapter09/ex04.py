# coding:utf-8

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    roles = db.relationship(
        'Role', backref='roles', lazy='dynamic')

    def __unicode__(self):
        return self.username

    # flask login expects an is_active method in your user model
    # you usually inactivate a user account if you don't want it
    # to have access to the system anymore
    def is_active(self):
        """
        Tells flask-login if the user account is active
        """
        return self.active


class Role(db.Model):
    """
    Holds our user roles
    """
    __tablename__ = 'roles'
    name = db.Column(db.String(60), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __unicode__(self):
        return self.name

# Flask and Flask-SQLAlchemy initialization here
admin = Admin()
admin.add_view(ModelView(User, db.session, category='Profile'))
admin.add_view(ModelView(Role, db.session, category='Profile'))


def app_factory(name=__name__):
    app = Flask(name)
    app.debug = True
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ex04.db'

    db.init_app(app)
    admin.init_app(app)
    return app


if __name__ == '__main__':
    app = app_factory()

    # we need to use a context here, otherwise we'll get a runtime error
    with app.test_request_context():
        db.drop_all()
        db.create_all()

    app.run()