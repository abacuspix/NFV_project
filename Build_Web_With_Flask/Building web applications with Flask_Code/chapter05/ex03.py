# coding:utf-8

from flask import Flask, render_template, redirect, flash
from flask_wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy

from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# define our model
class Employee(db.Model):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return 'employee %s' % self.name


db.create_all()

# auto-generate form for our model
EmployeeForm = model_form(Employee, base_class=Form)


@app.route("/", methods=['GET', 'POST'])
def index():
    # as you remember, request.POST is implicitly provided as argument
    form = EmployeeForm()

    try:
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            flash('New employee add to database')
            return redirect('/')
    except Exception, e:
        # log e
        db.session.rollback()
        flash('An error occurred accessing the database. Please, contact administration.')

    employee_list = Employee.query.all()
    return render_template('index.html', form=form, employee_list=employee_list)


if __name__ == '__main__':
    app.debug = True
    app.run()
