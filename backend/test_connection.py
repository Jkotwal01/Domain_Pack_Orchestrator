"""
Simple test script to verify MongoDB connection and basic functionality.
"""

import sys
sys.path.insert(0, 'd:/Anti/backend')

from db.connection import mongo_connection
from core.logging_config import logger

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("\n" + "="*60)
    print("Testing MongoDB Connection")
    print("="*60)
    
    success = mongo_connection.connect()
    
    if success:
        print("\n✓ MongoDB connection test PASSED")
        
        # Try to get database
        try:
            db = mongo_connection.get_database()
            print(f"✓ Database access successful: {db.name}")
            
            # Try to get collection
            collection = mongo_connection.get_collection()
            print(f"✓ Collection access successful: {collection.name}")
            
            return True
        except Exception as e:
            print(f"\n✗ Database access failed: {str(e)}")
            return False
    else:
        print("\n✗ MongoDB connection test FAILED")
        print("Please ensure MongoDB is installed and running on localhost:27017")
        return False

if __name__ == "__main__":
    test_mongodb_connection()
