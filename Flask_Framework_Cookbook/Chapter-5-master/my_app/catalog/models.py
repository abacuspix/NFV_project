from decimal import Decimal
from wtforms import StringField, DecimalField, SelectField, FileField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from wtforms.widgets import html_params, Select
from markupsafe import Markup
from flask_wtf import FlaskForm
from my_app import db


# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy='dynamic'))
    image_path = db.Column(db.String(255))

    def __init__(self, name, price, category, image_path):
        self.name = name
        self.price = price
        self.category = category
        self.image_path = image_path

    def __repr__(self):
        return f'<Product {self.id}: {self.name}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Category {self.id}: {self.name}>'


# Forms
class NameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])


# Custom Select Widget for CategoryField
class CustomCategoryInput(Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = []
        for val, label, selected in field.iter_choices():
            html.append(
                f'<input type="radio" {html_params(name=field.name, value=val, checked=selected, **kwargs)}> {label}'
            )
        return Markup(' '.join(html))


# CategoryField with Dynamic Choices
class CategoryField(SelectField):
    widget = CustomCategoryInput()

    def iter_choices(self):
        categories = [(c.id, c.name) for c in Category.query.all()]
        for value, label in categories:
            yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        if self.data not in [c.id for c in Category.query.all()]:
            raise ValidationError(self.gettext('Not a valid choice'))


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    price = DecimalField(
        'Price',
        validators=[InputRequired(), NumberRange(min=Decimal('0.0'))]
    )
    category = SelectField(
        'Category',
        validators=[InputRequired()]
    )
    image = FileField('Product Image')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Populate the category choices dynamically
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]


# Validator to Check Duplicate Categories
def check_duplicate_category(case_sensitive=True):
    def _check_duplicate(form, field):
        query = Category.query.filter(
            Category.name.ilike(field.data) if not case_sensitive else Category.name == field.data
        )
        if query.first():
            raise ValidationError(f'Category named "{field.data}" already exists.')
    return _check_duplicate


class CategoryForm(NameForm):
    name = StringField(
        'Name',
        validators=[InputRequired(), check_duplicate_category()]
    )
