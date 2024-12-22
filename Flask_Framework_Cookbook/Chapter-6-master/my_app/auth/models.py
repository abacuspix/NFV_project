from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from my_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pwdhash = db.Column(db.String(), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the provided password against the stored hash."""
        return check_password_hash(self.pwdhash, password)

    def get_id(self):
        """Returns the user's ID as a string."""
        return str(self.id)


class RegistrationForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField(
        'Password', [
            InputRequired(), EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])


class OpenIDForm(Form):
    openid = StringField('OpenID', [InputRequired()])
