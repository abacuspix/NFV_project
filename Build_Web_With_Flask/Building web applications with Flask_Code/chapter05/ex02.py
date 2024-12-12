# coding:utf-8

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:///employees.sqlite', echo=True)

# Base class for our models
Base = declarative_base()

# Create a session bound to the engine
Session = sessionmaker(bind=engine)
session = Session()


# Address Model
class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street = Column(String(100))
    number = Column(Integer)
    google_maps = Column(String(255))
    id_employee = Column(Integer, ForeignKey('employee.id'))

    def __repr__(self):
        return f"{self.street}, {self.number}"


# Employee Model
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    birthday = Column(Date)
    addresses = relationship("Address", backref="employee")

    def __repr__(self):
        return self.name


# Create the database tables
Base.metadata.create_all(engine)

# Uncomment this block to insert initial data
# session.add_all([
#     Employee(name='marcos mango', birthday=datetime.strptime('1990-09-06', '%Y-%m-%d')),
#     Employee(name='rosie rinn', birthday=datetime.strptime('1980-09-06', '%Y-%m-%d')),
#     Employee(name='mannie moon', birthday=datetime.strptime('1970-07-06', '%Y-%m-%d'))
# ])
# session.commit()

# session.add_all([
#     Address(street='Oak', number=399, google_maps='', id_employee=1),
#     Address(street='First Boulevard', number=1070, google_maps='', id_employee=1),
#     Address(street='Cleveland, OH', number=10,
#              google_maps='Cleveland,+OH,+USA/@41.4949426,-81.70586,11z', id_employee=2)
# ])
# session.commit()

# Get "marcos" and his addresses
marcos = session.query(Employee).filter(Employee.name.like(r"%marcos%")).first()

if marcos:
    # Extract the last name from the employee's name
    marcos_last_name = marcos.name.split(' ')[-1]
    print(marcos_last_name)
else:
    print("No employee found with the name matching 'marcos'.")
