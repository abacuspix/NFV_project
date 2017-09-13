# coding:utf-8

from sqlalchemy import create_engine

# we are connecting to a sqlite database called employees.db
# a sqlite database is a system file
engine = create_engine('sqlite:///employees.sqlite')

# given you have the appropriate driver installed
# for postgres: create_engine('postgresql://user:password@host_address/database_name')
# for oracle: create_engine('oracle://user:password@host_address/database_name')
# for mysql: create_engine('mysql://user:password@host_address/database_name')

# echo output to console (turn off on deploy)
engine.echo = True

# create our connection from the pool
conn = engine.connect()

conn.execute("""
CREATE TABLE employee (
  id          INTEGER PRIMARY KEY,
  name        STRING(100) NOT NULL,
  birthday    DATE NOT NULL
)""")

conn.execute("""
CREATE TABLE address(
  id      INTEGER PRIMARY KEY,
  street  STRING(100) NOT NULL,
  number  INTEGER,
  google_maps STRING(255),
  id_employee INTEGER NOT NULL,
  FOREIGN KEY(id_employee) REFERENCES employee(id)
)""")

# we start our transaction here
# all actions now are executed within the transaction context
trans = conn.begin()

try:
    # we are using a slightly different insertion syntax for convenience, here;
    # id value is not explicitly provided
    conn.execute("INSERT INTO employee (name, birthday) VALUES ('marcos mango', date('1990-09-06') );")
    conn.execute("INSERT INTO employee (name, birthday) VALUES ('rosie rinn', date('1980-09-06') );")
    conn.execute("INSERT INTO employee (name, birthday) VALUES ('mannie moon', date('1970-07-06') );")

    conn.execute(
        "INSERT INTO address (street, number, google_maps, id_employee) "
        "VALUES ('Oak', 399, '', 1)")
    conn.execute(
        "INSERT INTO address (street, number, google_maps, id_employee) "
        "VALUES ('First Boulevard', 1070, '', 1)")
    conn.execute(
        "INSERT INTO address (street, number, google_maps, id_employee) "
        "VALUES ('Cleveland, OH', 10, 'Cleveland,+OH,+USA/@41.4949426,-81.70586,11z', 2)")
    # commit all
    trans.commit()
except:
    # all or nothing. Undo what was executed within the transaction
    trans.rollback()
    raise

for row in conn.execute("SELECT * FROM employee WHERE strftime('%d', `birthday`) == '06' "):
    print "row:", row

# get marcos addresses
for row in conn.execute("""
  SELECT a.street, a.number FROM employee e
  LEFT OUTER JOIN address a
  ON e.id = a.id_employee
  WHERE e.name like '%marcos%';
  """):
    print "address:", row

# give connection back to the connection pool
conn.close()
