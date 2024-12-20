# coding:utf-8

from flask import Flask, flash, render_template, redirect, url_for, request, session, current_app
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import InputRequired

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login_view'
principal = Principal()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', backref='user', lazy=True)

    def is_active(self):
        return self.active


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()

    user = property(get_user)

    def validate_username(self, field):
        if self.user is None:
            raise ValidationError('Your username and password did not match')

    def validate_password(self, field):
        user = self.get_user()
        if user and user.password != self.password.data:
            raise ValidationError('Your username and password did not match')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user
        login_user(user)
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
        flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('login.html', form=form)


@login_required
def logout_view():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('login_view'))


def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))


def app_factory(config_class='config.Dev'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    principal.init_app(app)
    identity_loaded.connect(on_identity_loaded, app)
    return app


if __name__ == '__main__':
    app = app_factory()
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Example user and role
        user = User(username='admin', password='password', active=True)
        db.session.add(user)
        db.session.commit()
        role = Role(name='admin', user_id=user.id)
        db.session.add(role)
        db.session.commit()
    app.run()
