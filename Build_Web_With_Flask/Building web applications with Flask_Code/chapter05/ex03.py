# coding:utf-8

from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# Define the Employee model
class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'Employee {self.name}'


# Define the EmployeeForm manually
class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    birthday = DateField('Birthday (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Employee')


# Ensure tables are created within the application context
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = EmployeeForm()

    try:
        if form.validate_on_submit():
            # Create a new Employee object
            employee = Employee(
                name=form.name.data,
                birthday=form.birthday.data
            )
            db.session.add(employee)
            db.session.commit()
            flash('New employee added to the database!', 'success')
            return redirect('/')
    except Exception as e:
        # Log the error for debugging
        print(f"Error: {e}")
        db.session.rollback()
        flash('An error occurred accessing the database. Please contact administration.', 'danger')

    # Fetch all employees
    employee_list = Employee.query.all()
    return render_template('index.html', form=form, employee_list=employee_list)


if __name__ == '__main__':
    app.debug = True
    app.run()
