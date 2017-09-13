# coding:utf-8

from flask import Flask, flash, redirect, render_template
from flask_mongoengine import MongoEngine
from flask.ext.mongoengine.wtf import model_form
from flask_wtf import Form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MONGODB_SETTINGS'] = {
    # 'replicaset': '',
    'db': 'example',
    # 'host': '',
    # 'username': '',
    # 'password': ''
}
db = MongoEngine(app)


class Employee(db.Document):
    name = db.StringField()
    # montoengine does not support datefield
    birthday = db.DateTimeField()

    def __unicode__(self):
        return u'employee %s' % self.name


# auto-generate form for our model
EmployeeForm = model_form(Employee, base_class=Form, field_args={
    'birthday': {
        # we want to use date format, not datetime
        'format': '%Y-%m-%d'
    }
})


@app.route("/", methods=['GET', 'POST'])
def index():
    # as you remember, request.POST is implicitly provided as argument
    form = EmployeeForm()

    try:
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            employee.save()
            flash('New employee add to database')
            return redirect('/')
    except:
        # log e
        flash('An error occurred accessing the database. Please, contact administration.')

    employee_list = Employee.objects()
    return render_template('index.html', form=form, employee_list=employee_list)


if __name__ == '__main__':
    app.debug = True
    app.run()
