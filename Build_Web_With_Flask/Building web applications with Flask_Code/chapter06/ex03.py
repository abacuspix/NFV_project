# coding:utf-8

from flask import Flask, request, jsonify, render_template, url_for
from flask_wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf.csrf import CsrfProtect

from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite'

db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)

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


ArticleForm = model_form(Article, base_class=Form)
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/articles/", methods=["GET", "POST"])
@app.route("/articles/<int:article_id>", methods=["GET", "PUT", "DELETE"])
def articles(article_id=None):
    if request.method == "GET":
        if article_id:
            article = Article.query.get(article_id)

            if request.is_xhr:
                if article is None:
                    return jsonify({"msgs": ["the article you're looking for could not be found"]}), 404

                result = article_schema.dump(article)
                return jsonify({'article': result.data})

            return render_template('article.html', article=article, form=ArticleForm(obj=article))
        else:
            if request.is_xhr:
                # never return the whole set! As it would be very slow
                queryset = Article.query.limit(10)
                result = articles_schema.dump(queryset)

                # jsonify serializes our dict into a proper flask response
                return jsonify({"articles": result.data})
    elif request.method == "POST" and request.is_xhr:
        form = ArticleForm(request.form)

        if form.validate():
            article = Article()
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return jsonify({"msgs": ["article created"]})
        else:
            return jsonify({"msgs": ["the sent data is not valid"]}), 400

    elif request.method == "PUT" and request.is_xhr:
        article = Article.query.get(article_id)

        if article is None:
            return jsonify({"msgs": ["the article you're looking for could not be found"]}), 404

        form = ArticleForm(request.form, obj=article)

        if form.validate():
            form.populate_obj(article)
            db.session.add(article)
            db.session.commit()
            return jsonify({"msgs": ["article updated"]})
        else:
            return jsonify({"msgs": ["the sent data was not valid"]}), 400
    elif request.method == "DELETE" and request.is_xhr:
        article = Article.query.get(article_id)

        if article is None:
            return jsonify({"msgs": ["the article you're looking for could not be found"]}), 404

        db.session.delete(article)
        db.session.commit()
        return jsonify({"msgs": ["article removed"]})

    return render_template('articles.html', form=ArticleForm())

db.create_all()


if __name__ == '__main__':
    # we define the debug environment only if running through command line
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    app.run()