# coding:utf-8

from flask import Flask, jsonify, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define Article Model
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __str__(self):
        return self.content

    def url(self):
        return url_for('articles', article_id=self.id, _external=True)


# Marshmallow Schema for Serialization
class ArticleSchema(Schema):
    url = fields.Method("article_url")

    def article_url(self, article):
        return article.url()

    class Meta:
        fields = ('id', 'title', 'content', 'url')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/articles", methods=["GET"])
@app.route("/articles/<int:article_id>", methods=["GET"])
def articles(article_id=None):
    if article_id:
        article = Article.query.get(article_id)
        if not article:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"msgs": ["The article you're looking for could not be found"]}), 404
            else:
                abort(404)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({'article': article_schema.dump(article)})
        return render_template('article.html', article=article)

    queryset = Article.query.limit(10).all()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"articles": articles_schema.dump(queryset)})
    return render_template('articles.html', articles=queryset)


# Create database tables and populate with sample data
with app.app_context():
    db.create_all()
    if Article.query.count() == 0:
        article_a = Article(title='some title', content='some content')
        article_b = Article(title='other title', content='other content')

        db.session.add(article_a)
        db.session.add(article_b)
        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
