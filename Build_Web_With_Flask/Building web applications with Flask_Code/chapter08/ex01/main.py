# coding:utf-8

from flask import Flask
from database import db
from blog import app as blog_bp


def app_factory(name=None):
    app = Flask(name or __name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ex01.db'

    db.init_app(app)

    # let Flask know about blog blueprint
    app.register_blueprint(blog_bp)
    return app


if __name__ == '__main__':
    app = app_factory()
    app.debug = True

    # make sure our tables are created
    with app.test_request_context():
        db.create_all()

    app.run()