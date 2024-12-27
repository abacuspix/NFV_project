from flask import Flask
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__)
    # Add your app configurations here
    return app

cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()
