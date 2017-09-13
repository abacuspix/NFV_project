# coding:utf-8

"""
Example adapted from https://pythonhosted.org/Flask-Testing/#testing-with-liveserver
"""

import urllib2
from urlparse import urljoin
from selenium import webdriver
from flask import Flask, render_template, jsonify, url_for
from flask.ext.testing import LiveServerTestCase
from random import choice


my_lines = ['Hello there!', 'How do you do?', 'Flask is great, ain\'t it?']


def setup(app):
    @app.route("/")
    def index_view():
        return render_template('js_index.html')

    @app.route("/text")
    def text_view():
        return jsonify({'text': choice(my_lines)})


def app_factory(name=None):
    name = name or __name__
    app = Flask(name)
    setup(app)
    return app


class IndexTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()

    def tearDown(self):
        self.driver.close()

    def create_app(self):
        app = app_factory()
        app.config['TESTING'] = True
        # default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_server_is_up_and_running(self):
        resp = urllib2.urlopen(self.get_server_url())
        self.assertEqual(resp.code, 200)

    def test_random_text_was_loaded(self):
        with self.app.test_request_context():
            domain = self.get_server_url()
            path = url_for('.index_view')
            url = urljoin(domain, path)

            self.driver.get(url)
            fillme_element = self.driver.find_element_by_id('fillme')
            fillme_text = fillme_element.text
            self.assertIn(fillme_text, my_lines)


if __name__ == '__main__':
    import unittest
    unittest.main()