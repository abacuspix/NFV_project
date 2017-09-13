# coding:utf-8

import tempfile, os
import json
from random import choice

from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
names = ['Marie', 'Rosie', 'John', 'Marcus']
surnames = ['Mango', 'Doe', 'Little', 'Candy']


def new_user(**kw):
    kw['name'] = kw.get('name', "%s %s" % (choice(names), choice(surnames)) )
    kw['gender'] = kw.get('gender', choice(['M', 'F', 'U']))
    return kw


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(1), default='U')

    def __unicode__(self):
        return self.name


def app_factory(name=None):
    name = name or __name__
    app = Flask(name)
    return app


class MyTestCase(TestCase):
    def create_app(self):
        app = app_factory()
        app.config['TESTING'] = True
        # db_fd: database file descriptor
        # we create a temporary file to hold our data
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        db.init_app(app)
        return app

    def load_fixture(self, path, model_cls):
        """
        Loads a json fixture into the database
        """
        fixture = json.load(open(path))

        for data in fixture:
            # Model accepts dict like parameter
            instance = model_cls(**data)
            # makes sure our session knows about our new instance
            db.session.add(instance)

        db.session.commit()

    def setUp(self):
        db.create_all()
        # you could load more fixtures if needed
        self.load_fixture('fixtures/users.json', User)

    def tearDown(self):
        # makes sure the session is removed
        db.session.remove()

        # close file descriptor
        os.close(self.db_fd)

        # delete temporary database file
        # as SQLite database is a single file, this is equivalent to a drop_all
        os.unlink(self.app.config['DATABASE'])

    def test_fixture(self):
        marie = User.query.filter(User.name.ilike('Marie%')).first()
        self.assertEqual(marie.gender, "F")

if __name__ == '__main__':
    import unittest
    unittest.main()