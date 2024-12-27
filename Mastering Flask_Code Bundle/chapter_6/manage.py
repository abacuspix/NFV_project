import os
from flask_migrate import Migrate, upgrade, init, migrate
from webapp import create_app
from webapp.models import db, User, Post, Tag, Comment
from manage import manager
# Default to development configuration
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app(f'webapp.config.{env.capitalize()}Config')
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command("db", MigrateCommand)
# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Flask CLI commands
@app.cli.command("create_db")
def create_db():
    """Creates the database."""
    try:
        db.create_all()
        print("Database created.")
    except Exception as e:
        print(f"Error creating database: {e}")

@app.cli.command("drop_db")
def drop_db():
    """Drops the database."""
    try:
        db.drop_all()
        print("Database dropped.")
    except Exception as e:
        print(f"Error dropping database: {e}")

@app.cli.command("seed_db")
def seed_db():
    """Seeds the database with sample data."""
    try:
        user1 = User(username="admin", password="password")
        user2 = User(username="guest", password="guestpass")
        post1 = Post(title="First Post", text="This is the first post.", user=user1)
        post2 = Post(title="Guest Post", text="This is a post by the guest user.", user=user2)
        tag1 = Tag(title="Flask")
        tag2 = Tag(title="Python")

        post1.tags.extend([tag1, tag2])
        post2.tags.append(tag2)

        db.session.add_all([user1, user2, post1, post2])
        db.session.commit()
        print("Database seeded with initial data.")
    except Exception as e:
        print(f"Error seeding database: {e}")


@app.cli.command("migrate_db")
def migrate_db():
    """Runs Flask-Migrate commands."""
    os.system("flask db init")
    os.system("flask db migrate")
    os.system("flask db upgrade")
    print("Database migrations applied.")

# Run the application
if __name__ == "__main__":
    app.run()
