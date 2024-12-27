from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic'
    )
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title, text, publish_date, user_id):
        self.title = title
        self.text = text
        self.publish_date = publish_date
        self.user_id = user_id

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __init__(self, name, text, date, post_id):
        self.name = name
        self.text = text
        self.date = date
        self.post_id = post_id

    def __repr__(self):
        return f"<Comment '{self.text[:15]}'>"


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"<Tag '{self.title}'>"
