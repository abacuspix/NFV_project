from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import your app and database
from main import app, db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Provide shell context for Flask CLI."""
    return {
        "app": app,
        "db": db,
        # Add your models here
        # "User": User,
        # "Post": Post,
    }

if __name__ == "__main__":
    app.run()
