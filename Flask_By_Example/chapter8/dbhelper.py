import datetime
import pymysql
import dbconfig


class DBHelper:

    def connect(self, database="crimemap"):
        """Establish a database connection."""
        print("Getting connection")
        return pymysql.connect(
            host='localhost',
            user=dbconfig.db_user,
            passwd=dbconfig.db_password,
            db=database
        )

    def add_crime(self, category, date, latitude, longitude, desc):
        """Add a crime entry to the database."""
        connection = self.connect()
        try:
            query = """INSERT INTO crimes (category, date, latitude, longitude, description) 
                       VALUES (%s, %s, %s, %s, %s)"""
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longitude, desc))
                connection.commit()
        except Exception as e:
            print(f"An error occurred while adding the crime: {e}")
        finally:
            connection.close()

    def get_all_crimes(self):
        """Retrieve all crime entries from the database."""
        connection = self.connect()
        try:
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()  # Fetch all rows at once

            named_crimes = []
            for crime in results:
                named_crime = {
                    'latitude': crime[0],
                    'longitude': crime[1],
                    'date': datetime.datetime.strftime(crime[2], '%Y-%m-%d'),
                    'category': crime[3],
                    'description': crime[4]
                }
                named_crimes.append(named_crime)
            return named_crimes
        except Exception as e:
            print(f"An error occurred while retrieving crimes: {e}")
            return []
        finally:
            connection.close()
