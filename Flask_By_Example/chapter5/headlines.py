import feedparser
from flask import Flask, render_template, request, make_response
import datetime
import json
from urllib.parse import quote
from urllib.request import urlopen

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"

DEFAULTS = {
    'publication': 'bbc',
    'city': 'London,UK',
    'currency_from': 'GBP',
    'currency_to': 'USD'
}


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")
def home():
    # Get customized headlines
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    # Get customized weather
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # Get customized currency
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    # Save cookies and return template
    response = make_response(render_template("home.html", articles=articles,
                                             weather=weather, currency_from=currency_from,
                                             currency_to=currency_to, rate=rate, currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_rate(frm, to):
    """
    Fetches currency exchange rate from `frm` to `to`.
    """
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates', {})
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    if frm_rate and to_rate:
        return (to_rate / frm_rate, parsed.keys())
    return (None, parsed.keys())


def get_news(publication):
    """
    Fetches news from the selected RSS feed.
    """
    feed = feedparser.parse(RSS_FEEDS[publication.lower()])
    return feed['entries']


def get_weather(query):
    """
    Fetches weather information for the given city.
    """
    query = quote(query)
    url = WEATHER_URL.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {
            'description': parsed['weather'][0]['description'],
            'temperature': parsed['main']['temp'],
            'city': parsed['name'],
            'country': parsed['sys']['country']
        }
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
