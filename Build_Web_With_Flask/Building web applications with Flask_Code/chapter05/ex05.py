# coding:utf-8

from flask import Flask, flash, redirect, render_template, request
from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MONGODB_SETTINGS'] = {
    'db': 'example'
}

db = MongoEngine(app)


# Define the Employee model
class Employee(db.Document):
    name = db.StringField(required=True)
    birthday = db.DateTimeField(required=True)

    def __str__(self):
        return f'Employee {self.name}'


# Define the EmployeeForm manually
class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Employee')


@app.route("/", methods=['GET', 'POST'])
def index():
    form = EmployeeForm()

    try:
        if form.validate_on_submit():
            # Create a new Employee object
            employee = Employee(
                name=form.name.data,
                birthday=datetime.combine(form.birthday.data, datetime.min.time())
            )
            employee.save()
            flash('New employee added to the database', 'success')
            return redirect('/')
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        flash('An error occurred accessing the database. Please contact administration.', 'danger')

    # Query all employees
    employee_list = Employee.objects()
    return render_template('index.html', form=form, employee_list=employee_list)


if __name__ == '__main__':
    app.debug = True
    app.run()
