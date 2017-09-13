# coding:utf-8

from flask import Flask, jsonify, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __unicode__(self):
        return self.content

    def url(self):
        return url_for('.articles', article_id=self.id)


# we use marshmallow Schema to serialize our articles
class ArticleSchema(Schema):
    """
    Article dict serializer
    """

    url = fields.Method("article_url")

    def article_url(self, article):
        return article.url()

    class Meta:
        # which fields should be serialized?
        fields = ('id', 'title', 'content', 'url')


article_schema = ArticleSchema()
# many -> allow for object list dump
articles_schema = ArticleSchema(many=True)


@app.route("/articles", methods=["GET"])
@app.route("/articles/<article_id>", methods=["GET"])
def articles(article_id=None):
    if article_id:
        article = Article.query.get(article_id)

        if request.is_xhr:
            if article is None:
                return jsonify({"msgs": ["the article you're looking for could not be found"]}), 404

            result = article_schema.dump(article)
            return jsonify({'article': result})
        else:
            if article is None:
                abort(404)

            return render_template('article.html', article=article)
    else:
        queryset = Article.query.limit(10)

        if request.is_xhr:
            # never return the whole set! As it would be very slow
            result = articles_schema.dump(queryset)

            # jsonify serializes our dict into a proper flask response
            return jsonify({"articles": result.data})
        else:
            return render_template('articles.html', articles=queryset)


db.create_all()

# let's populate our database with some data; empty examples are not that cool
if Article.query.count() == 0:
    article_a = Article(title='some title', content='some content')
    article_b = Article(title='other title', content='other content')

    db.session.add(article_a)
    db.session.add(article_b)
    db.session.commit()

if __name__ == '__main__':
    # we define the debug environment only if running through command line
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    app.run()
