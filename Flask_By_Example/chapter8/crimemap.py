import datetime
import json
import string

import dateparser
from flask import Flask, render_template, request

import dbconfig

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper


app = Flask(__name__)
DB = DBHelper()

categories = ['mugging', 'break-in']


def sanitize_string(userinput):
    whitelist = string.ascii_letters + string.digits + " !?.,;:-'()&"
    return ''.join(filter(lambda x: x in whitelist, userinput))


def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None


@app.route("/")
def home(error_message=None):
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
        return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)
    except Exception as e:
        print(f"An error occurred while loading the home page: {e}")
        return render_template("home.html", crimes=[], categories=categories, error_message="Error loading data.")


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    try:
        category = request.form.get("category")
        if category not in categories:
            return home("Invalid category selected.")

        date = format_date(request.form.get("date"))
        if not date:
            return home("Invalid date. Please use yyyy-mm-dd format.")

        try:
            latitude = float(request.form.get("latitude"))
            longitude = float(request.form.get("longitude"))
        except ValueError:
            return home("Latitude and Longitude must be valid numbers.")

        description = sanitize_string(request.form.get("description"))
        DB.add_crime(category, date, latitude, longitude, description)
        return home()
    except Exception as e:
        print(f"An error occurred while submitting the crime: {e}")
        return home("An unexpected error occurred. Please try again later.")


if __name__ == '__main__':
    app.run(debug=True)  # Disable debug mode in production
