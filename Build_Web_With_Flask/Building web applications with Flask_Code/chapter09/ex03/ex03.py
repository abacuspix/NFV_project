# coding:utf-8

from flask_wtf import Form

from wtforms import StringField, PasswordField, ValidationError
from wtforms import validators

from flask import Flask, flash, render_template, redirect, url_for, request, session, current_app
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user
from flask.ext.principal import Principal, Permission, Identity, AnonymousIdentity, identity_changed
from flask.ext.principal import RoleNeed, UserNeed, identity_loaded


principal = Principal()
login_manager = LoginManager()
login_manager.login_view = 'login_view'
# you may also overwrite the default flashed login message
# login_manager.login_message = 'Please log in to access this page.'
db = SQLAlchemy()

# Create a permission with a single Need
# we use it to see if an user has the correct rights to do something
admin_permission = Permission(RoleNeed('admin'))


# UserMixin implements some of the methods required by Flask-Login
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    roles = db.relationship(
        'Role', backref='roles', lazy='dynamic')

    def __unicode__(self):
        return self.username

    # flask login expects an is_active method in your user model
    # you usually inactivate a user account if you don't want it
    # to have access to the system anymore
    def is_active(self):
        """
        Tells flask-login if the user account is active
        """
        return self.active


class Role(db.Model):
    """
    Holds our user roles
    """
    __tablename__ = 'roles'
    name = db.Column(db.String(60), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __unicode__(self):
        return self.name


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


class Config(object):
    "Base configuration class"
    DEBUG = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ex03.db'


class Dev(Config):
    "Our dev configuration"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/dev.db'


def setup(app):
    # initializing our extensions ; )
    db.init_app(app)
    principal.init_app(app)
    login_manager.init_app(app)

    # adding views without using decorators
    app.add_url_rule('/admin/', view_func=admin_view)
    app.add_url_rule('/admin/context/', view_func=admin_only_view)
    app.add_url_rule('/login/', view_func=login_view, methods=['GET', 'POST'])
    app.add_url_rule('/logout/', view_func=logout_view)

    # connecting on_identity_loaded signal to our app
    # you may also connect using the @identity_loaded.connect_via(app) decorator
    identity_loaded.connect(on_identity_loaded, app, False)


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
    return User.query.get(userid)


def on_identity_loaded(sender, identity):
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


def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        # authenticate the user...
        login_user(form.user)

        # Tell Flask-Principal the identity changed
        identity_changed.send(
            # do not use current_app directly
            current_app._get_current_object(),
            identity=Identity(form.user.id))
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("admin_view"))

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
    return redirect(request.args.get('next') or '/')


# I like this approach better ...
@login_required
@admin_permission.require()
def admin_view():
    """
    Only admins can access this
    """
    return render_template('admin.html')


# Meh ...
@login_required
def admin_only_view():
    """
    Only admins can access this
    """
    with admin_permission.require():
        # using context
        return render_template('admin.html')


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