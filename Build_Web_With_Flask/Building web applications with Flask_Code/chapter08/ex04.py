# coding:utf-8

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'  # required for session cookies to work
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True

toolbar = DebugToolbarExtension(app)


@app.route("/")
def index_view():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()