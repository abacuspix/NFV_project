from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL, ValidationError
from webapp.models import User


class CommentForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('Content', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if not user or not user.check_password(self.password.data):
            raise ValidationError('Invalid username or password')


class OpenIDForm(FlaskForm):
    openid = StringField('OpenID URL', validators=[DataRequired(), URL()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    recaptcha = RecaptchaField()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("User with that name already exists")
