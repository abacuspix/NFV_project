from app import app, db
import admin # This line is new, plimport models
import models
import views
import api

from urlparse import urljoin
from flask import request, url_for
from werkzeug.contrib.atom import AtomFeed
from models import Entry

from entries.blueprint import entries
app.register_blueprint(entries, url_prefix='/entries')
from snippets.blueprint import snippets
app.register_blueprint(snippets, url_prefix='/snippets')



@app.route('/latest.atom')
def recent_feed():
    feed = AtomFeed(
        'Latest Blog Posts',
        feed_url=request.url,
        url=request.url_root,
        author=request.url_root
    )
    entries = Entry.query.filter(Entry.status == Entry.STATUS_PUBLIC).order_by(Entry.created_timestamp.desc()).limit(15).all()
    for entry in entries:
        feed.add(
            entry.title,
            entry.body,
            content_type='html',
            url=urljoin(request.url_root, url_for("entries.detail", slug=entry.slug) ),
            updated=entry.modified_timestamp,
            published=entry.created_timestamp
        )
    return feed.get_response()

if __name__ == '__main__':
    app.run()
