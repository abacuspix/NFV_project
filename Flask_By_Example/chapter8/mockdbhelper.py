class MockDBHelper:

    def connect(self, database="crimemap"):
        """Mock connect method."""
        print(f"Mock connection to database: {database}")

    def add_crime(self, category, date, latitude, longitude, description):
        """Mock add_crime method to simulate adding a crime."""
        data = [category, date, latitude, longitude, description]
        for i in data:
            print(i, type(i))

    def get_all_crimes(self):
        """Mock get_all_crimes method to simulate fetching crimes."""
        return [{
            'latitude': -33.301304,
            'longitude': 26.523355,
            'date': "2000-01-01",
            'category': "mugging",
            'description': "mock description"
        }]

    def add_input(self, data):
        """Mock add_input method."""
        print(f"Mock add_input called with data: {data}")

    def clear_all(self):
        """Mock clear_all method."""
        print("Mock clear_all called, all mock data cleared.")
