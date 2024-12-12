# coding:utf-8

from sqlalchemy import create_engine, text

# Connect to a SQLite database
engine = create_engine('sqlite:///employees.sqlite', echo=True)

# Create a connection
conn = engine.connect()

# Create tables
conn.execute(text("""
CREATE TABLE IF NOT EXISTS employee (
  id          INTEGER PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  birthday    DATE NOT NULL
)
"""))

conn.execute(text("""
CREATE TABLE IF NOT EXISTS address (
  id      INTEGER PRIMARY KEY,
  street  VARCHAR(100) NOT NULL,
  number  INTEGER,
  google_maps VARCHAR(255),
  id_employee INTEGER NOT NULL,
  FOREIGN KEY(id_employee) REFERENCES employee(id)
)
"""))

# Perform database operations within a transaction
try:
    # Insert data into employee table
    conn.execute(
        text("INSERT INTO employee (name, birthday) VALUES (:name, :birthday)"),
        [{"name": "marcos mango", "birthday": "1990-09-06"},
         {"name": "rosie rinn", "birthday": "1980-09-06"},
         {"name": "mannie moon", "birthday": "1970-07-06"}]
    )

    # Insert data into address table
    conn.execute(
        text(
            "INSERT INTO address (street, number, google_maps, id_employee) "
            "VALUES (:street, :number, :google_maps, :id_employee)"
        ),
        [
            {"street": "Oak", "number": 399, "google_maps": "", "id_employee": 1},
            {"street": "First Boulevard", "number": 1070, "google_maps": "", "id_employee": 1},
            {"street": "Cleveland, OH", "number": 10, "google_maps": "Cleveland,+OH,+USA/@41.4949426,-81.70586,11z", "id_employee": 2}
        ]
    )

    # Commit the transaction
    conn.commit()
except Exception as e:
    # Rollback the transaction in case of an error
    conn.rollback()
    print(f"Error: {e}")
    raise

# Fetch employees with birthdays on the 6th day of any month
for row in conn.execute(text("SELECT * FROM employee WHERE strftime('%d', birthday) = '06'")):
    print("row:", row)

# Fetch addresses for "marcos mango"
for row in conn.execute(text("""
  SELECT a.street, a.number FROM employee e
  LEFT OUTER JOIN address a
  ON e.id = a.id_employee
  WHERE e.name LIKE '%marcos%'
""")):
    print("address:", row)

# Close the connection
conn.close()
