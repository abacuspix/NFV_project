# coding:utf-8

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees1.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


# Define the Article model
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content}


# Define the Article Resource
class ArticleResource(Resource):
    def get(self, article_id=None):
        if article_id:
            article = Article.query.get(article_id)
            if not article:
                return {"message": "Article not found"}, 404
            return article.to_dict(), 200
        articles = Article.query.all()
        return [article.to_dict() for article in articles], 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ("title", "content")):
            return {"message": "Invalid data"}, 400
        article = Article(title=data["title"], content=data["content"])
        db.session.add(article)
        db.session.commit()
        return article.to_dict(), 201

    def put(self, article_id):
        article = Article.query.get(article_id)
        if not article:
            return {"message": "Article not found"}, 404
        data = request.get_json()
        if not data:
            return {"message": "Invalid data"}, 400
        article.title = data.get("title", article.title)
        article.content = data.get("content", article.content)
        db.session.commit()
        return article.to_dict(), 200

    def delete(self, article_id):
        article = Article.query.get(article_id)
        if not article:
            return {"message": "Article not found"}, 404
        db.session.delete(article)
        db.session.commit()
        return {"message": "Article deleted"}, 200


# Register the Article Resource
api.add_resource(ArticleResource, "/api/articles", "/api/articles/<int:article_id>")

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
