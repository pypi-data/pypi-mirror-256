from pymongo import MongoClient
from uuid_extensions import uuid7str
from pymongo.server_api import ServerApi

# Generate a UUID using the UUID7 strategy.
def uuid_id():
    return uuid7str()

# Initialize and return the MongoDB collection.
def initialize_collection(uri, db_name, collection_name):
    """
    Initialize and return the MongoDB collection.
    """
    try:
        client = MongoClient(uri)
        return client[db_name][collection_name]
    except Exception as e:
        return f"Error initializing collection: {str(e)}"

# Initialize and return the MongoDB collection.
def initialize_collection_with_certificate(uri, certificate_path, db_name, collection_name):
    """
    Initialize and return the MongoDB collection using TLS certificate authentication.
    
    Parameters:
    - uri: MongoDB URI string.
    - certificate_path: Path to the TLS certificate file.
    - db_name: Name of the MongoDB database.
    - collection_name: Name of the collection within the database.
    
    Returns:
    - MongoDB collection object.
    """
    try:
        # Initialize MongoClient with TLS certificate authentication
        client = MongoClient(uri,
                             tls=True,
                             tlsCertificateKeyFile=certificate_path,
                             server_api=ServerApi('1'))
        
        # Access the specified database and collection
        return client[db_name][collection_name]
    
    except Exception as e:
        return f"Error initializing collection with certificate: {str(e)}"

# Insert data into the MongoDB collection.
def set_data(collection, data):
    """
    Insert data into the MongoDB collection.
    """
    try:
        return collection.insert_one(data)
    except Exception as e:
        return f"Error setting data: {str(e)}"

# Retrieve data from the MongoDB collection where 'available' is True.
def get_data(collection):
    """
    Retrieve data from the MongoDB collection where 'available' is True.
    """
    try:
        return collection.find({'available': True})
    except Exception as e:
        return f"Error getting data: {str(e)}"

# Retrieve all data from the MongoDB collection.
def get_all_data(collection):
    """
    Retrieve all data from the MongoDB collection.
    """
    try:
        return collection.find()
    except Exception as e:
        return f"Error getting all data: {str(e)}"

# Retrieve a single document from the MongoDB collection by its ID.
def get_data_one(collection, id_data):
    """
    Retrieve a single document from the MongoDB collection by its ID.
    """
    try:
        return collection.find_one({'_id': id_data})
    except Exception as e:
        return f"Error getting data by ID: {str(e)}"

# Remove data from the MongoDB collection by its ID and set 'available' to False.
def remove_data_bool(collection, id_data):
    """
    Remove data from the MongoDB collection by its ID and set 'available' to False.
    """
    try:
        return collection.update_one({'_id': id_data}, {'$set': {'available': False}})
    except Exception as e:
        return f"Error removing data (bool): {str(e)}"

# Remove data from the MongoDB collection by its ID.
def remove_data(collection, id_data):
    """
    Remove data from the MongoDB collection by its ID.
    """
    try:
        return collection.delete_one({'_id': id_data})
    except Exception as e:
        return f"Error removing data: {str(e)}"

# Update data in the MongoDB collection by its ID.
def update_data(collection, id_data, data):
    """
    Update data in the MongoDB collection by its ID.
    """
    try:
        return collection.update_one({'_id': id_data}, {'$set': data})
    except Exception as e:
        return f"Error updating data: {str(e)}"

# Delete all data from the MongoDB collection.
def delete_db(collection):
    """
    Delete all data from the MongoDB collection.
    """
    try:
        return collection.delete_many({})
    except Exception as e:
        return f"Error deleting database: {str(e)}"

# Count documents in the MongoDB collection where 'available' is True.
def count_db_bool(collection):
    """
    Count documents in the MongoDB collection where 'available' is True.
    """
    try:
        return collection.count_documents({'available': True})
    except Exception as e:
        return f"Error counting documents (bool): {str(e)}"

# Count all documents in the MongoDB collection.
def count_all_db(collection):
    """
    Count all documents in the MongoDB collection.
    """
    try:
        return collection.count_documents({})
    except Exception as e:
        return f"Error counting all documents: {str(e)}"

# Retrieve data from the MongoDB collection based on a specific field and its value.
def search_data_by_field(collection, field_name, field_value):
    """
    Retrieve data from the MongoDB collection based on a specific field and its value.
    """
    try:
        return collection.find({field_name: field_value})
    except Exception as e:
        return f"Error searching data by field: {str(e)}"

# Update existing data if found, or insert new data if not found.
def upsert_data(collection, query, data):
    """
    Update existing data if found, or insert new data if not found.
    """
    try:
        return collection.update_one(query, {'$set': data}, upsert=True)
    except Exception as e:
        return f"Error upserting data: {str(e)}"

# Search across all fields of the MongoDB collection and return matching documents.
def search_across_fields(collection, search_query):
    """
    Search across all fields of the MongoDB collection and return matching documents.
    """
    try:
        return collection.find({ "$or": [{field: { "$regex": search_query, "$options": "i" }} for field in collection.find_one().keys()]})
    except Exception as e:
        return f"Error searching across fields: {str(e)}"

# Search for the given term in all fields of the MongoDB collection.
def search_all_fields(collection, search_term):
    """
    Search for the given term in all fields of the MongoDB collection.
    """
    try:
        return collection.find({ "$or": [{key: {"$regex": search_term.lower(), "$options": "i"}} for key in collection.find_one().keys()]})
    except Exception as e:
        return f"Error searching all fields: {str(e)}"

# Close the connection to the MongoDB database.
def close_connection(collection):
    """
    Close the connection to the MongoDB database.
    """
    try:
        return collection.client.close()
    except Exception as e:
        return f"Error closing connection: {str(e)}"
