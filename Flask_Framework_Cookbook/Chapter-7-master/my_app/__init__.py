from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test7.db'  # Adjust path as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
app.secret_key = 'some_random_key'

# Initialize extensions
db = SQLAlchemy(app)
api = Api(app)

# Import and register blueprints
from my_app.catalog.views import catalog
app.register_blueprint(catalog)

# Create database tables
with app.app_context():  # Ensure the app context is active
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
