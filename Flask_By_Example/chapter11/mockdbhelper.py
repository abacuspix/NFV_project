import datetime

MOCK_USERS = [
    {
        "email": "test@example.com",
        "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
        "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e",
    }
]
MOCK_TABLES = [
    {"_id": "1", "number": "1", "owner": "t@t.com", "url": "mockurl"}
]
MOCK_REQUESTS = [
    {"_id": "1", "table_number": "1", "table_id": "1", "time": datetime.datetime.now()}
]


class MockDBHelper:

    def get_user(self, email):
        """Retrieve a user by email."""
        user = next((x for x in MOCK_USERS if x.get("email") == email), None)
        print(f"Queried user: {user}")  # Debugging output
        return user

    def add_user(self, email, salt, hashed):
        """Add a new user."""
        MOCK_USERS.append({"email": email, "salt": salt, "hashed": hashed})

    def add_table(self, number, owner):
        """Add a new table."""
        table_id = str(number)
        MOCK_TABLES.append({"_id": table_id, "number": number, "owner": owner, "url": None})
        return table_id

    def update_table(self, _id, url):
        """Update the URL of a table."""
        table = self.get_table(_id)
        if table:
            table["url"] = url

    def get_tables(self, owner_id):
        """Retrieve all tables for a specific owner."""
        return [table for table in MOCK_TABLES if table["owner"] == owner_id]

    def get_table(self, table_id):
        """Retrieve a specific table by ID."""
        return next((table for table in MOCK_TABLES if table["_id"] == table_id), None)

    def delete_table(self, table_id):
        """Delete a table by its ID."""
        self._delete_item(MOCK_TABLES, "_id", table_id)

    def add_request(self, table_id, time):
        """Add a new request."""
        table = self.get_table(table_id)
        if not table:
            raise ValueError(f"Table with ID {table_id} not found.")
        MOCK_REQUESTS.append(
            {
                "_id": table_id,
                "owner": table["owner"],
                "table_number": table["number"],
                "table_id": table_id,
                "time": time,
            }
        )
        return True

    def get_requests(self, owner_id):
        """Retrieve all requests for a specific owner."""
        return [request for request in MOCK_REQUESTS if request.get("owner") == owner_id]

    def delete_request(self, request_id):
        """Delete a request by its ID."""
        self._delete_item(MOCK_REQUESTS, "_id", request_id)

    @staticmethod
    def _delete_item(collection, key, value):
        """Generic method to delete an item from a collection."""
        for i, item in enumerate(collection):
            if item.get(key) == value:
                del collection[i]
                break
