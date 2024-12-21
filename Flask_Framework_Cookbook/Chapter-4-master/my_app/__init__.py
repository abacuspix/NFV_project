from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set a unique and secure secret key
app.secret_key = 'your_unique_secret_key_here'

db = SQLAlchemy(app)

# Register blueprints
from my_app.catalog.views import catalog
app.register_blueprint(catalog)

# Ensure database tables are created inside application context
with app.app_context():
    db.create_all()