# coding:utf-8

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define the Article model
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    def __str__(self):
        return self.content


# Marshmallow Schema for serialization
class ArticleSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/articles", methods=["GET"])
@app.route("/articles/<int:article_id>", methods=["GET"])
def articles(article_id=None):
    if article_id:
        article = Article.query.get(article_id)
        if article is None:
            return jsonify({"msgs": ["The article you're looking for could not be found"]}), 404

        result = article_schema.dump(article)
        return jsonify({'article': result})
    else:
        # Fetch a limited number of articles
        queryset = Article.query.limit(10).all()
        result = articles_schema.dump(queryset)
        return jsonify({"articles": result})


# Create database tables if not exist
with app.app_context():
    db.create_all()

    # Populate the database if empty
    if Article.query.count() == 0:
        article_a = Article(title='some title', content='some content')
        article_b = Article(title='other title', content='other content')

        db.session.add(article_a)
        db.session.add(article_b)
        db.session.commit()


if __name__ == '__main__':
    app.config['SQLALCHEMY_ECHO'] = True
    app.debug = True
    app.run()
