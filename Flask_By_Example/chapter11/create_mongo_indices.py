import pymongo

# Initialize MongoDB client and database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['waitercaller']

# Create unique index for the 'users' collection
user_index = db.users.create_index("email", unique=True)
print(f"Unique index created for users collection: {user_index}")

# Create unique index for the 'requests' collection
request_index = db.requests.create_index("table_id", unique=True)
print(f"Unique index created for requests collection: {request_index}")
