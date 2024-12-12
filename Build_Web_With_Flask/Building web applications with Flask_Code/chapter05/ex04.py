# coding:utf-8

from datetime import datetime
from mongoengine import *

# Connect to the MongoDB database (assumes MongoDB is running locally)
connect('example')


# Define the Employee model
class Employee(Document):
    name = StringField(required=True)
    birthday = DateTimeField(required=True)

    def __str__(self):
        return f'Employee {self.name}'


# Create an employee instance
employee = Employee(
    name='rosie rinn',
    birthday=datetime.strptime('1980-09-06', '%Y-%m-%d')
)
employee.save()

# Query for employees with "rosie" in their name
for e in Employee.objects(name__icontains='rosie'):
    print(e)
