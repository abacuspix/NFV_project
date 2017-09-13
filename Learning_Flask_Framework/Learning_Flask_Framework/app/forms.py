import wtforms
from wtforms import validators
from models import User

class LoginForm(wtforms.Form):
    email = wtforms.StringField("Email",
        validators=[validators.DataRequired()])
    password = wtforms.PasswordField("Password",
        validators=[validators.DataRequired()])
    remember_me = wtforms.BooleanField("Remember me?",
        default=True)
        
    def validate(self):
        if not super(LoginForm, self).validate():
            return False
            
        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False
        return True

from models import Snippet

class SnippetForm(wtforms.Form):
    title = wtforms.StringField('Title',
    validators=[validators.DataRequired()])
    body = wtforms.TextAreaField('Body',
    validators=[validators.DataRequired()])
    status = wtforms.SelectField(
        'Entry status',
        choices=(
        (Snippet.STATUS_PUBLIC, 'Public'),
        (Snippet.STATUS_DRAFT, 'Draft')),
        coerce=int)
        
    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry
