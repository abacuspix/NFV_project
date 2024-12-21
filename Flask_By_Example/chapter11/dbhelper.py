import pymongo
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

DATABASE = "waitercaller"


class DBHelper:

    def __init__(self, uri="mongodb://localhost:27017/"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[DATABASE]

    def get_user(self, email):
        """Retrieve a user by email."""
        return self.db.users.find_one({"email": email})

    def add_user(self, email, salt, hashed):
        """Add a new user to the database."""
        try:
            self.db.users.insert_one({"email": email, "salt": salt, "hashed": hashed})
        except DuplicateKeyError:
            print(f"User with email {email} already exists.")

    def add_table(self, number, owner):
        """Add a new table."""
        result = self.db.tables.insert_one({"number": number, "owner": owner})
        return result.inserted_id

    def update_table(self, _id, url):
        """Update a table's URL."""
        self.db.tables.update_one({"_id": ObjectId(_id)}, {"$set": {"url": url}})

    def get_tables(self, owner_id):
        """Retrieve all tables owned by a user."""
        return list(self.db.tables.find({"owner": owner_id}))

    def get_table(self, table_id):
        """Retrieve a specific table by its ID."""
        try:
            return self.db.tables.find_one({"_id": ObjectId(table_id)})
        except Exception as e:
            print(f"Error retrieving table with ID {table_id}: {e}")
            return None

    def delete_table(self, table_id):
        """Delete a table by its ID."""
        try:
            self.db.tables.delete_one({"_id": ObjectId(table_id)})
        except Exception as e:
            print(f"Error deleting table with ID {table_id}: {e}")

    def add_request(self, table_id, time):
        """Add a new request."""
        table = self.get_table(table_id)
        if not table:
            print(f"Table with ID {table_id} not found.")
            return False
        try:
            self.db.requests.insert_one({
                "owner": table['owner'],
                "table_number": table['number'],
                "table_id": table_id,
                "time": time
            })
            return True
        except DuplicateKeyError:
            print(f"Duplicate request for table {table_id}.")
            return False

    def get_requests(self, owner_id):
        """Retrieve all requests for a specific owner."""
        return list(self.db.requests.find({"owner": owner_id}))

    def delete_request(self, request_id):
        """Delete a specific request by its ID."""
        try:
            self.db.requests.delete_one({"_id": ObjectId(request_id)})
        except Exception as e:
            print(f"Error deleting request with ID {request_id}: {e}")
