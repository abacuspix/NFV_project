# coding:utf-8

from flask import Flask, url_for, request
import unittest


def setup_database(app):
    # setup database ...
    pass


def setup(app):
    from flask import request, render_template

    # this is not a good production setup
    # you should register blueprints here
    @app.route("/")
    def index_view():
        return render_template('index.html', name=request.args.get('name'))


def app_factory(name=__name__, debug=True):
    app = Flask(name)
    app.debug = debug
    setup_database(app)
    setup(app)
    return app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        # setUp is called before each test method
        # we create a clean app for each test
        self.app = app_factory()
        # we create a clean client for each test
        self.client = self.app.test_client()

    def tearDown(self):
        # release resources here
        # usually, you clean or destroy the test database
        pass

    def test_index_no_arguments(self):
        with self.app.test_request_context():
            path = url_for('index_view')
            resp = self.client.get(path)
            # check response content
            self.assertIn('Hello World', resp.data)

    def test_index_with_name(self):
        with self.app.test_request_context():
            name = 'Amazing You'
            path = url_for('index_view', name=name)
            resp = self.client.get(path)
            # check response content
            self.assertIn(name, resp.data)


if __name__ == '__main__':
    unittest.main()