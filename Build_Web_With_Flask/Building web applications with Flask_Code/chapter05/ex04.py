# coding:utf-8

from datetime import datetime

from mongoengine import *

# as the mongo daemon, mongod, is running locally, we just need the database name to connect
connect('example')


class Employee(Document):
    name = StringField()
    birthday = DateTimeField()

    def __unicode__(self):
        return u'employee %s' % self.name


employee = Employee()
employee.name = 'rosie rinn'
employee.birthday = datetime.strptime('1980-09-06', '%Y-%m-%d')
employee.save()

for e in Employee.objects(name__contains='rosie'):
    print e
