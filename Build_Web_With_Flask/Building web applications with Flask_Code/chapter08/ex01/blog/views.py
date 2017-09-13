# coding:utf-8

from models import *
from flask import Blueprint, render_template, request

app = Blueprint(
    'blog',  # our blueprint name and route prefix
    __name__, template_folder='templates'
)


@app.route("/")
@app.route("/<slug>")
def posts_view(slug=None):
    if slug is not None:
        post = Post.query.filter_by(slug=slug).first()
        return render_template('post.html', post=post)

    # lets paginate our result
    page_number = int(request.args.get('page', 1))
    page = Post.query.paginate(page_number, 10)

    return render_template('posts.html', page=page)