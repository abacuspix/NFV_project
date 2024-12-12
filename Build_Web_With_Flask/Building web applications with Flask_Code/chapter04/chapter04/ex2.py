# coding:utf-8

from wtforms import Form, ValidationError
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired
from werkzeug.datastructures import MultiDict
import re


def is_proper_username(form, field):
    if not re.match(r"^\w+$", field.data):
        msg = f'{field.name} should have any of these characters only: a-z0-9_'
        raise ValidationError(msg)


class LoginForm(Form):
    username = StringField(
        u'Username:', [InputRequired(), is_proper_username, Length(min=3, max=40)]
    )
    password = PasswordField(
        u'Password:', [InputRequired(), Length(min=5, max=12)]
    )

    def validate_password(self, field):
        data = field.data
        if not re.findall('.*[a-z].*', data):
            msg = f'{field.name} should have at least one lowercase character'
            raise ValidationError(msg)
        # Has at least one uppercase character
        if not re.findall('.*[A-Z].*', data):
            msg = f'{field.name} should have at least one uppercase character'
            raise ValidationError(msg)
        # Has at least one number
        if not re.findall('.*[0-9].*', data):
            msg = f'{field.name} should have at least one number'
            raise ValidationError(msg)
        # Has at least one special character
        if not re.findall('.*[^ a-zA-Z0-9].*', data):
            msg = f'{field.name} should have at least one special character'
            raise ValidationError(msg)


# Example usage with empty input
form = LoginForm(MultiDict({}))
print(form.validate())
print(form.errors)
