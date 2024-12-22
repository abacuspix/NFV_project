import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an env variable for production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'some_random_key')  # Secure for production

db = SQLAlchemy(app)

# Blueprint registration
from my_app.catalog.views import catalog
app.register_blueprint(catalog)

# Database initialization
with app.app_context():
    db.create_all()
