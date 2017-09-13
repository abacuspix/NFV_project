# coding:utf-8

import lxml.html

from flask.ext.testing import TestCase
from flask import url_for
from main import app_factory
from database import db


class BaseTest(object):
    """
    Base test case. Our test cases should extend this class.
    It handles database creation and clean up.
    """

    def create_app(self):
        app = app_factory()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/ex01_test.sqlite'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class PostDetailTest(BaseTest, TestCase):
    def add_single_post(self):
        from blog import Post

        db.session.add(Post(title='Some text', slug='some-text', content='some content'))
        db.session.commit()

        assert Post.query.count() == 1

    def setUp(self):
        super(PostDetailTest, self).setUp()
        self.add_single_post()

    def test_get_request(self):
        with self.app.test_request_context():
            url = url_for('blog.posts_view', slug='some-text')
            resp = self.client.get(url)
            self.assert200(resp)
            self.assertTemplateUsed('post.html')
            self.assertIn('Some text', resp.data)


class PostListTest(BaseTest, TestCase):
    def add_posts(self):
        from blog import Post

        db.session.add_all([
            Post(title='Some text', slug='some-text', content='some content'),
            Post(title='Some more text', slug='some-more-text', content='some more content'),
            Post(title='Here we go', slug='here-we-go', content='here we go!'),
        ])
        db.session.commit()

        assert Post.query.count() == 3

    def add_multiple_posts(self, count):
        from blog import Post

        db.session.add_all([
            Post(title='%d' % i, slug='%d' % i, content='content %d' % i) for i in range(count)
        ])
        db.session.commit()

        assert Post.query.count() == count

    def test_get_posts(self):
        self.add_posts()

        # as we want to use url_for ...
        with self.app.test_request_context():
            url = url_for('blog.posts_view')
            resp = self.client.get(url)

            self.assert200(resp)
            self.assertIn('Some text', resp.data)
            self.assertIn('Some more text', resp.data)
            self.assertIn('Here we go', resp.data)
            self.assertTemplateUsed('posts.html')

    def test_page_number(self):
        self.add_multiple_posts(15)

        with self.app.test_request_context():
            url = url_for('blog.posts_view')
            resp = self.client.get(url)

            self.assert200(resp)

            # we use lxml to count how many li results were returned
            handle = lxml.html.fromstring(resp.data)
            self.assertEqual(10, len(handle.xpath("//ul/li")))


if __name__ == '__main__':
    import unittest

    unittest.main()