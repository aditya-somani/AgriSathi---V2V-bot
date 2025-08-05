# Purpose: Simple MongoDB database manager for agricultural query requests

import random
import datetime
from typing import Optional, Dict, List
import logging
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import string

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reduce MongoDB debug logs verbosity
logging.getLogger("pymongo").setLevel(logging.WARNING)

class DatabaseManager:
    """
    Simple MongoDB database manager for agricultural query requests
    """
    
    def __init__(self, connection_string: str = None, database_name: str = "agricultural_assistant"):
        """
        Initialize MongoDB database manager
        
        Args:
            connection_string (str): MongoDB connection string
            database_name (str): Name of the MongoDB database
        """
        # Get MongoDB connection string from environment or use default
        self.connection_string = connection_string or os.getenv(
            "MONGODB_CONNECTION_STRING", 
            "mongodb://localhost:27017/"
        ) 
        self.database_name = database_name # name of the database
        self.client = None
        self.db = None
        self.queries_collection = None
        
        try:
            # Initialize MongoDB client with timeout settings
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,         # 10 second connection timeout
                socketTimeoutMS=10000,          # 10 second socket timeout
            ) # initialize the client
            
            self.db = self.client[self.database_name] # initialize the database
            
            # Test connection with timeout
            self.client.admin.command('ping') # test the connection
            logger.info(f"Successfully connected to MongoDB: {self.database_name}") # log the successful connection
            
            # Initialize collections and indexes
            self.init_database() # initialize the database
            logger.info("Database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}") # log the error
            logger.error(f"Connection string attempted: {self.connection_string}")
            # Clean up any partial connections
            if self.client:
                try:
                    self.client.close()
                except:
                    pass
            self.client = None
            self.db = None
            self.queries_collection = None
            raise
    
    def init_database(self) -> None:
        """
        Initialize MongoDB collections with basic indexes.
        Only creates indexes if the collection doesn't already exist.
        """
        try:
            # Check if the queries collection already exists
            existing_collections = self.db.list_collection_names() # list all the collections in the database
            collection_exists = "queries" in existing_collections # check if the queries collection exists
            
            # Get reference to the queries collection (this doesn't create the collection physically)
            self.queries_collection = self.db.queries # get the queries collection
            
            if collection_exists:
                # Collection already exists - no need to create indexes again
                logger.info("Collection 'queries' already exists - skipping index creation")
            else:
                # Collection doesn't exist - create indexes (this will also create the collection)
                logger.info("Creating 'queries' collection with required indexes")
                
                # Create basic indexes (Atlas compatible)
                # request_code is unique and mobile is a regular index and created_at is a descending index
                self.queries_collection.create_index("request_code", unique=True) # unique index on request_code
                self.queries_collection.create_index("mobile") # regular index on mobile  
                self.queries_collection.create_index([("created_at", -1)]) # descending index on created_at
                
                logger.info("Collection and indexes created successfully")
            
        except Exception as e: # if there is an error
            logger.error(f"Failed to initialize MongoDB: {e}") # log the error
            raise # re-raise the same exception that was just caught
    
    def generate_request_code(self) -> str:
        """
        Generate a simple 6-digit request code
        
        Returns:
            str: 6-digit request code
        """
        while True: # keep generating codes until a unique one is found
            # Generate random code
            hex_chars = string.hexdigits.upper() # get all the hex characters - uppercase
            code = f"{''.join(random.choice(hex_chars) for _ in range(6))}" # generate a random code
            
            # Check if code already exists
            existing = self.queries_collection.find_one({"request_code": code}) # check if the code already exists
            if not existing: # if the code does not exist
                return code # return the code
    
    def create_query(self, name: str, mobile: str, location: str, description: str) -> str:
        """
        Create a new query request
        
        Args:
            name (str): Customer's name
            mobile (str): Customer's mobile number
            location (str): Customer's location
            description (str): Query description
            
        Returns:
            str: 6 character hex request code , like A1B2C3
            
        Raises:
            ValueError: If validation fails
            Exception: If database operation fails
        """
        # Check database connection first
        if not self.is_connected():
            logger.error("Database connection not available when creating query")
            raise Exception("Database connection not available")
        
        # Basic validation
        if not all([name.strip(), mobile.strip(), location.strip(), description.strip()]): # if any of the fields are empty
            raise ValueError("All fields are required") # raise an error
        
        # Clean mobile number
        mobile_clean = ''.join(filter(str.isdigit, mobile)) # remove all non-digit characters
        if len(mobile_clean) < 10 or mobile_clean[0] not in '6789': # if the mobile number is less than 10 digits or does not start with 6,7,8,9
            raise ValueError("Invalid mobile number - must be 10 digits starting with 6, 7, 8, or 9") # raise an error
            
        try:
            # Generate request code
            request_code = self.generate_request_code() # generate a request code
            
            # Create query document
            query_doc = {
                "request_code": request_code, # request code
                "name": name.strip(), # name
                "mobile": mobile_clean, # mobile number
                "location": location.strip(), # location
                "description": description.strip(), # description
                "status": "pending", # status
                "created_at": datetime.datetime.now(datetime.timezone.utc), # created at - in UTC timezone not indian timezone
                "expert_assigned": None, # expert assigned
                "notes": None # notes
            }
            
            # Insert into MongoDB
            result = self.queries_collection.insert_one(query_doc) # insert the query document into the database
            
            if result.inserted_id: # if the query is inserted successfully
                logger.info(f"Query created successfully: {request_code} for mobile: {mobile_clean[:4]}****") 
                return request_code 
            else: # if the query is not inserted successfully
                raise Exception("Failed to insert query into database") # raise an error
                
        except ValueError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            logger.error(f"Failed to create query: {e}") 
            raise Exception(f"Database error while creating query: {str(e)}")
    
    def get_query_status(self, request_code: str) -> Optional[Dict]:
        """
        Get query status by request code
        
        Args:
            request_code (str): 6 character hex request code
            
        Returns:
            Optional[Dict]: Query information or None if not found
        """
        try:
            query = self.queries_collection.find_one({"request_code": request_code}) # find the query by request code
            
            if query: # if the query is found
                # Format for display
                query['_id'] = str(query['_id']) # convert the _id to a string
                if query.get('created_at'): # if the created at is not None
                    query['created_at'] = query['created_at'].strftime('%Y-%m-%d %H:%M:%S') # convert the created at to a string
                return query
            
            return None # if the query is not found
                
        except Exception as e:
            logger.error(f"Failed to get query status: {e}")
            raise
    
    
    def close_connection(self):
        """Close MongoDB connection"""
        try:
            if hasattr(self, 'client'): # if the client exists
                self.client.close() # close the client
                logger.info("MongoDB connection closed") # log the successful closing of the connection
        except Exception as e:
            logger.error(f"Error closing MongoDB: {e}") # log the error

    def test_connection_and_permissions(self) -> dict:
        """
        Test database connection and basic operations for debugging
        
        Returns:
            dict: Detailed test results
        """
        results = {
            "connection_status": False,
            "database_accessible": False,
            "collection_accessible": False,
            "can_insert": False,
            "can_query": False,
            "error_details": [],
            "connection_info": {
                "connection_string": self.connection_string,
                "database_name": self.database_name
            }
        }
        
        try:
            # Test 1: Basic connection
            if self.client is not None:
                self.client.admin.command('ping')
                results["connection_status"] = True
            else:
                results["error_details"].append("MongoDB client not initialized")
                return results
                
            # Test 2: Database access
            if self.db is not None:
                collections = self.db.list_collection_names()
                results["database_accessible"] = True
            else:
                results["error_details"].append("Database not accessible")
                return results
                
            # Test 3: Collection access
            if self.queries_collection is not None:
                # Try to count documents (should work even if collection is empty)
                count = self.queries_collection.count_documents({})
                results["collection_accessible"] = True
                results["current_query_count"] = count
            else:
                results["error_details"].append("Queries collection not accessible")
                return results
                
            # Test 4: Insert test (create a test document)
            test_doc = {
                "test": True,
                "timestamp": datetime.datetime.now(datetime.timezone.utc),
                "test_id": "connection_test"
            }
            test_result = self.queries_collection.insert_one(test_doc)
            if test_result.inserted_id:
                results["can_insert"] = True
                # Clean up test document
                self.queries_collection.delete_one({"_id": test_result.inserted_id})
            else:
                results["error_details"].append("Failed to insert test document")
                
            # Test 5: Query test
            existing_count = self.queries_collection.count_documents({"status": "pending"})
            results["can_query"] = True
            results["pending_queries_count"] = existing_count
            
        except Exception as e:
            results["error_details"].append(f"Connection test failed: {str(e)}")
            
        return results

    def is_connected(self) -> bool:
        """
        Check if database connection is active
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            if self.client is None or self.db is None:
                return False
            # Quick ping test
            self.client.admin.command('ping')
            return True
        except Exception:
            return False

try:
    db_manager = DatabaseManager() # initialize the database manager
except Exception as e:
    logger.error(f"Failed to initialize database manager: {e}")
    db_manager = None
