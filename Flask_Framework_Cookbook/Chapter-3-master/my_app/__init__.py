from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_app.catalog.views import catalog
from my_app.database import Base, engine
from my_app.catalog.models import Product


# Flask application
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

# Initialize SQLAlchemy
Base.metadata.create_all(engine)

# Register Blueprint
app.register_blueprint(catalog)
