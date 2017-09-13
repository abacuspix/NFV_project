# coding:utf-8

from flask import Flask, render_template, redirect, flash, request
from flask_wtf import Form
from wtforms import ValidationError
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired

import re

app = Flask(__name__)
app.secret_key = '"\xba)\x96\xc6nt\x00\x0c%4\x0f\x9f\xc1(5\xc48\xb3\xb5\x95\xfa%D'


def is_proper_username(form, field):
    if not re.match(r"^\w+$", field.data):
        msg = '%s should have any of these characters only: a-z0-9_' % field.name
        raise ValidationError(msg)


class LoginForm(Form):
    username = StringField(
        u'Username:', [InputRequired(), is_proper_username, Length(min=3, max=40)])
    password = PasswordField(
        u'Password:', [InputRequired(), Length(min=5, max=12)])

    @staticmethod
    def validate_password(form, field):
        data = field.data
        if not re.findall('.*[a-z].*', data):
            msg = '%s should have at least one lowercase character' % field.name
            raise ValidationError(msg)
        # has at least one uppercase character
        if not re.findall('.*[A-Z].*', data):
            msg = '%s should have at least one uppercase character' % field.name
            raise ValidationError(msg)
        # has at least one number
        if not re.findall('.*[0-9].*', data):
            msg = '%s should have at least one number' % field.name
            raise ValidationError(msg)
        # has at least one special character
        if not re.findall('.*[^ a-zA-Z0-9].*', data):
            msg = '%s should have at least one special character' % field.name
            raise ValidationError(msg)


@app.route('/', methods=['get', 'post'])
def login_view():
    # msg is no longer necessary. We will use flash, instead
    form = LoginForm()

    if form.validate_on_submit():
        flash('Username and password are correct')
        # it's good practice to redirect after a successful form submit
        return redirect('/')
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()
