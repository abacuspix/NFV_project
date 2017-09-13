# coding:utf-8

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

engine = create_engine('sqlite:///employees.sqlite')
engine.echo = True

# base class for our models
Base = declarative_base()

# we create a session binded to our engine
Session = sessionmaker(bind=engine)

# and then the session itself
session = Session()


# our first model
class Address(Base):
    # the table name we want in the database
    __tablename__ = 'address'

    # our primary key
    id = Column(Integer, primary_key=True)
    street = Column(String(100))
    number = Column(Integer)
    google_maps = Column(String(255))
    # our foreign key to employee
    id_employee = Column(Integer, ForeignKey('employee.id'))

    def __repr__(self):
        return u"%s, %d" % (self.street, self.number)


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    birthday = Column(Date)
    # we map
    addresses = relationship("Address", backref="employee")

    def __repr__(self):
        return self.name


# create our database from our classes
Base.metadata.create_all(engine)

# # execute everything inside a transaction
# session.add_all([
#         Employee(name='marcos mango', birthday=datetime.strptime('1990-09-06', '%Y-%m-%d')),
#         Employee(name='rosie rinn', birthday=datetime.strptime('1980-09-06', '%Y-%m-%d')),
#         Employee(name='mannie moon', birthday=datetime.strptime('1970-07-06', '%Y-%m-%d'))
#     ])
# session.commit()

# session.add_all([
#     Address(street='Oak', number=399, google_maps='', id_employee=1),
#     Address(street='First Boulevard', number=1070, google_maps='', id_employee=1),
#     Address(street='Cleveland, OH', number=10,
#              google_maps='Cleveland,+OH,+USA/@41.4949426,-81.70586,11z', id_employee=2)
# ])
# session.commit()

# # get marcos, then his addresses
# marcos = session.query(Employee).filter(Employee.name.like(r"%marcos%")).first()
# for address in marcos.addresses:
#     print 'Address:', address

# marcos.name = "marcos tangerine"
# session.commit()
marcos = session.query(Employee).filter(Employee.name.like(r"%marcos%")).first()
marcos_last_name = marcos.name.split(' ')[-1]
print marcos_last_name
