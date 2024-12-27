from flask import Flask
from flask_login import current_user, LoginManager
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_openid import OpenID

# Replace these with actual module imports
from models import db
from extensions import oid
from controllers.main import main_blueprint
from controllers.blog import blog_blueprint

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
principals = Principal()

def create_app(object_name):
    """
    A Flask application factory.

    Arguments:
        object_name: The Python path of the config object,
                     e.g. project.config.ProdConfig
    """

    app = Flask(__name__)
    app.config.from_object(object_name)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = "main.login"

    # Set up identity loader
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint)

    return app

if __name__ == '__main__':
    # Replace with your configuration
    app = create_app('project.config.ProdConfig')
    app.run(debug=True)
