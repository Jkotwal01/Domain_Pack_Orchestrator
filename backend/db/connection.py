"""
MongoDB connection management module.
Handles database connection, validation, and graceful shutdown.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from core.config import settings
from core.logging_config import logger
from typing import Optional


class MongoDBConnection:
    """
    Singleton MongoDB connection manager.
    Ensures only one connection instance exists throughout the application.
    """
    
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def connect(self) -> bool:
        """
        Establish connection to MongoDB with validation.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info(f"Attempting to connect to MongoDB at {settings.MONGODB_URI}")
            
            # Create MongoDB client with timeout
            self._client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            
            # Validate connection by pinging the server
            self._client.admin.command('ping')
            
            # Success message to console and log
            success_msg = f"✓ MongoDB connected successfully to {settings.DATABASE_NAME}"
            print(f"\n{success_msg}\n")
            logger.info(success_msg)
            
            return True
            
        except ConnectionFailure as e:
            error_msg = f"MongoDB connection failed: {str(e)}"
            logger.error(error_msg)
            print(f"\n✗ {error_msg}\n")
            return False
            
        except ServerSelectionTimeoutError as e:
            error_msg = f"MongoDB server selection timeout: {str(e)}"
            logger.error(error_msg)
            print(f"\n✗ {error_msg}\n")
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error connecting to MongoDB: {str(e)}"
            logger.error(error_msg)
            print(f"\n✗ {error_msg}\n")
            return False
    
    def get_database(self):
        """
        Get the database instance.
        
        Returns:
            Database: MongoDB database instance
            
        Raises:
            RuntimeError: If connection not established
        """
        try:
            if self._client is None:
                raise RuntimeError("MongoDB connection not established. Call connect() first.")
            
            db = self._client[settings.DATABASE_NAME]
            logger.debug(f"Retrieved database: {settings.DATABASE_NAME}")
            return db
            
        except Exception as e:
            logger.error(f"Error getting database: {str(e)}")
            raise
    
    def get_collection(self):
        """
        Get the YAML configs collection.
        
        Returns:
            Collection: MongoDB collection instance
        """
        try:
            db = self.get_database()
            collection = db[settings.COLLECTION_NAME]
            logger.debug(f"Retrieved collection: {settings.COLLECTION_NAME}")
            return collection
            
        except Exception as e:
            logger.error(f"Error getting collection: {str(e)}")
            raise
    
    def close(self):
        """
        Close MongoDB connection gracefully.
        """
        try:
            if self._client:
                self._client.close()
                logger.info("MongoDB connection closed successfully")
                print("\n✓ MongoDB connection closed\n")
                
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")


# Global connection instance
mongo_connection = MongoDBConnection()


def get_database():
    """
    Convenience function to get database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    return mongo_connection.get_database()


def get_collection():
    """
    Convenience function to get collection instance.
    
    Returns:
        Collection: MongoDB collection instance
    """
    return mongo_connection.get_collection()
