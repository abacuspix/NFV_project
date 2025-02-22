import feedparser
from flask import Flask, render_template

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    # Validate publication
    if publication not in RSS_FEEDS:
        publication = "bbc"
    
    # Parse the RSS feed
    feed = feedparser.parse(RSS_FEEDS[publication])
    
    # Handle empty feed
    if not feed['entries']:
        return render_template("error.html", message="No articles found.")
    
    # Get the first article
    first_article = feed['entries'][0]
    return render_template(
        "news.html",
        title=first_article.get("title"),
        published=first_article.get("published"),
        summary=first_article.get("summary")
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
