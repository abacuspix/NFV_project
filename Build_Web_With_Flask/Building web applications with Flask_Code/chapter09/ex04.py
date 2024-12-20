# coding:utf-8

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# User model
class User(db.Model, UserMixin):
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
        Tells Flask-Login if the user account is active
        """
        return self.active


# Role model
class Role(db.Model):
    """
    Holds user roles
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)  # Added unique integer primary key
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Role(name={self.name}, user_id={self.user_id})>"


# Initialize Flask-Admin
admin = Admin(name="Admin Interface", template_mode="bootstrap3")
admin.add_view(ModelView(User, db.session, category="Profile"))
admin.add_view(ModelView(Role, db.session, category="Profile"))


def app_factory(name=__name__):
    """
    Factory function to create and configure the Flask app
    """
    app = Flask(name)
    app.debug = True
    app.config['SECRET_KEY'] = 'secret'  # Use an environment variable for security in production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Set to False for performance
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ex04.db'

    # Initialize extensions
    db.init_app(app)
    admin.init_app(app)
    return app


if __name__ == '__main__':
    app = app_factory()

    # Create the database and tables
    with app.app_context():
        db.drop_all()  # Only for development; remove in production
        db.create_all()

    # Run the Flask app
    app.run()
