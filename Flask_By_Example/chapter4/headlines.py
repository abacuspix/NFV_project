import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests
from urllib.parse import quote
#import urllib2
from urllib.request import urlopen

CURRENCY_URL = "https://api.exchangerate-api.com/v4/latest/USD"

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=b23c94daab584f4580e4e2bf75cbcf7e"

DEFAULTS = {'publication': 'bbc',
            'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }


@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    # get customised weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    # get customised currency based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    return render_template("home.html", articles=articles, weather=weather,
                           currency_from=currency_from, currency_to=currency_to, rate=rate,
                           currencies=sorted(currencies))


def get_rate(currency_from, currency_to):
    """
    Fetches the exchange rate between two currencies.
    """
    all_currency = urlopen(CURRENCY_URL).read()
    data = json.loads(all_currency)
    rates = data.get("rates", {})
    rate_from = rates.get(currency_from, 1)
    rate_to = rates.get(currency_to, 1)
    return rate_to / rate_from, rates


def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(city):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=YOUR_API_KEY"
    query = quote(city)  # Correctly use `quote` from `urllib.parse`
    url = api_url.format(query)
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
