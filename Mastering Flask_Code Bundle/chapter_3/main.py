import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from sqlalchemy import func
from config import DevConfig
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Association table for many-to-many relationship
tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship(
        'Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic')
    )

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    def __repr__(self):
        return f"<Tag '{self.title}'>"


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('Comment', validators=[DataRequired()])


def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = (
        db.session.query(Tag, func.count(tags.c.post_id).label('total'))
        .join(tags)
        .group_by(Tag)
        .order_by(func.count(tags.c.post_id).desc())
        .limit(5)
        .all()
    )
    return recent, top_tags


@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html', posts=posts, recent=recent, top_tags=top_tags
    )


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            name=form.name.data,
            text=form.text.data,
            post_id=post_id,
            date=datetime.datetime.now()
        )
        db.session.add(new_comment)
        db.session.commit()

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'post.html', post=post, tags=tags, comments=comments, recent=recent, top_tags=top_tags, form=form
    )


@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html', tag=tag, posts=posts, recent=recent, top_tags=top_tags
    )


@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html', user=user, posts=posts, recent=recent, top_tags=top_tags
    )


if __name__ == '__main__':
    app.run(debug=True)
