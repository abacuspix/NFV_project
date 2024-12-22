import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# Configure upload folder and database URI
#app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'my_app', 'static', 'uploads')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'

# Set Flask secret key
app.secret_key = 'some_random_key'

# Initialize the database
db = SQLAlchemy(app)

# Register blueprints
from my_app.catalog.views import catalog
app.register_blueprint(catalog)

# Create tables inside the app context
with app.app_context():
    db.create_all()
