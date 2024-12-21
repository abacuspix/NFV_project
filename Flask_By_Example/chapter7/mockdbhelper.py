class MockDBHelper:

    def connect(self, database="crimemap"):
        # Mock method; no actual database connection
        pass

    def add_crime(self, category, date, latitude, longitude, description):
        # Print inputs and their types for testing
        data = [category, date, latitude, longitude, description]
        for i in data:
            print(i, type(i))

    def get_all_crimes(self):
        # Return mock data for testing
        return [{
            'latitude': -33.301304,
            'longitude': 26.523355,
            'date': "2000-01-01",
            'category': "mugging",
            'description': "mock description"
        }]

    def add_input(self, data):
        # Mock method for adding data; no real operation
        print(f"Mock add input: {data}")

    def clear_all(self):
        # Mock method to clear data; no real operation
        print("Mock clear all data")
