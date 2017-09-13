# coding:utf-8

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