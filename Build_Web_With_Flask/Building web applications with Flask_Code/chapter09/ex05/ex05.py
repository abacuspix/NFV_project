# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, ValidationError
from wtforms import validators

from flask import Flask, flash, render_template, redirect, url_for, request, session, current_app

from flask.ext.login import LoginManager, login_user, logout_user
from flask.ext.principal import Identity, AnonymousIdentity, identity_changed
from flask.ext.principal import identity_loaded

from admin import *
from permissions import *
from database import *
from config import *

login_manager = LoginManager()
login_manager.login_view = 'login_view'


class LoginForm(Form):
    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

    user = property(get_user)

    username = StringField(validators=[validators.InputRequired()])
    password = PasswordField(validators=[validators.InputRequired()])

    def validate_username(self, field):
        "Validates that the username belongs to an actual user"
        if self.user is None:
            # do not send a very specifc error message here, otherwise you'll
            # be telling the user which users are available in your database
            raise ValidationError('Your username and password did not match')

    def validate_password(self, field):
        username = field.data
        user = User.query.get(username)

        if user is not None:
            if not user.password == field.data:
                raise ValidationError('Your username and password did not match')


def setup_admin(app):
    # initializing our extensions ; )
    admin.init_app(app)
    admin.add_view(AuthModelView(User, db.session, category='Profile'))
    admin.add_view(AuthModelView(Role, db.session, category='Profile'))


def setup_principal(app):
    principal.init_app(app)
    identity_loaded.connect(on_identity_loaded, app, False)


def setup_database(app):
    db.init_app(app)


def setup_login_manager(app):
    login_manager.init_app(app)


def setup(app):
    setup_admin(app)
    setup_database(app)
    setup_principal(app)
    setup_login_manager(app)

    # adding views without using decorators
    app.add_url_rule('/login/', view_func=login_view, methods=['GET', 'POST'])
    app.add_url_rule('/logout/', view_func=logout_view)


def on_identity_loaded(sender, identity):
    with sender.app_context():
        # Set the identity user object
        identity.user = current_user

        # in case you have resources that belong to a specific user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))


# our application factory
def app_factory(name=__name__, config=Dev):
    app = Flask(name)
    app.config.from_object(config)
    setup(app)
    return app


# we use the decorator to let the login_manager know of our load_user
# userid is the model id by default
@login_manager.user_loader
def load_user(userid):
    """
    Loads an user using the user_id

    Used by flask-login to load the user with the user id stored in session
    """
    user = User.query.get(userid)
    return user


def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        # authenticate the user...
        user = form.user
        login_user(user)

        # Tell Flask-Principal the identity changed
        identity_changed.send(
            # do not use current_app directly
            current_app._get_current_object(),
            identity=Identity(user.id))
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("admin.index"))

    return render_template("login.html", form=form)


@login_required  # you can't logout if you're not logged
def logout_view():
    # Remove the user information from the session
    # Flask-Login can handle this on it's own = ]
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())

    # it's good practice to redirect after logout
    return redirect(request.args.get('next') or url_for('login_view'))


def populate():
    """
    Populates our database with a single user, for testing ; )

    Why not use fixtures? Just don't wanna ...
    """
    user = User(username='student', password='passwd', active=True)
    db.session.add(user)
    db.session.commit()
    role = Role(name='admin', user_id=user.id)
    db.session.add(role)
    db.session.commit()


if __name__ == '__main__':
    app = app_factory()

    # we need to use a context here, otherwise we'll get a runtime error
    with app.test_request_context():
        db.drop_all()
        db.create_all()
        populate()

    app.run()