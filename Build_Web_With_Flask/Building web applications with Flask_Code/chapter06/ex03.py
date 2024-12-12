# coding:utf-8

from flask import Flask, jsonify, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees1.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define Article Model
class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(255), nullable=False)

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


# Define ArticleForm using Flask-WTF
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route("/articles/", methods=["GET", "POST"])
@app.route("/articles/<int:article_id>", methods=["GET", "PUT", "DELETE"])
def articles(article_id=None):
    if request.method == "GET":
        if article_id:
            article = Article.query.get(article_id)
            if not article:
                return jsonify({"msgs": ["The article you're looking for could not be found"]}), 404

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({'article': article_schema.dump(article)})
            return render_template('article.html', article=article, form=ArticleForm(obj=article))

        queryset = Article.query.limit(10).all()
        form = ArticleForm()  # Create an instance of the form
        return render_template('articles.html', articles=queryset, form=form)  # Pass form to the template
    elif request.method == "POST":
        form = ArticleForm()
        if form.validate_on_submit():
            article = Article(title=form.title.data, content=form.content.data)
            db.session.add(article)
            db.session.commit()
            return jsonify({"msgs": ["Article created"]}), 201
        return jsonify({"msgs": ["Invalid data"]}), 400

    elif request.method == "DELETE":
        article = Article.query.get(article_id)
        if not article:
            return jsonify({"msgs": ["The article you're looking for could not be found"]}), 404

        db.session.delete(article)
        db.session.commit()
        return jsonify({"msgs": ["Article removed"]}), 200

    return render_template('articles.html', form=ArticleForm())


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
