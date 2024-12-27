from flask import Flask
from flask_script import Manager, Server  # Replace flask.ext.script with flask_script
from main import app

# Initialize Flask-Script manager
manager = Manager(app)
manager.add_command("server", Server())

# Add shell context
@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == "__main__":
    manager.run()
