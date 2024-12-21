from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.fields import EmailField
from wtforms import validators


class RegistrationForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(),
            validators.Length(min=8, message="Please choose a password of at least 8 characters")
        ]
    )
    password2 = PasswordField(
        'Confirm Password',
        validators=[
            validators.DataRequired(),
            validators.EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    loginemail = EmailField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email()
        ]
    )
    loginpassword = PasswordField(
        'Password',
        validators=[
            validators.DataRequired(message="Password field is required")
        ]
    )
    submit = SubmitField('Login')


class CreateTableForm(FlaskForm):
    tablenumber = StringField(
        'Table Number',
        validators=[
            validators.DataRequired()
        ]
    )
    submit = SubmitField('Create Table')
