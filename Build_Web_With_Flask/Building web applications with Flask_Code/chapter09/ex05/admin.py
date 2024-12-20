# coding:utf-8

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    User model for managing users in the application.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Increased length for hashed passwords
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User(username={self.username}, active={self.active})>"

    def is_active(self):
        """
        Indicates whether the user account is active.
        """
        return self.active


class Role(db.Model):
    """
    Role model for managing user roles.
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)  # Added a unique primary key
    name = db.Column(db.String(60), nullable=False)  # Changed primary key to a regular column
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Role(name={self.name}, user_id={self.user_id})>"
