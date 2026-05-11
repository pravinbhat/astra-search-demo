"""
AstraDB Data API client wrapper.
Handles connection and operations with AstraDB.
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from astrapy import DataAPIClient
from astrapy.exceptions import DataAPIException

from app.config import settings

logger = logging.getLogger(__name__)


class AstraDBClient:
    """Wrapper class for AstraDB Data API operations."""
    
    def __init__(self):
        """Initialize AstraDB client."""
        self.client = None
        self.database = None
        self.collection = None
        self._connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to AstraDB.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Initialize the client
            self.client = DataAPIClient(settings.astra_db_application_token)
            
            # Get database instance
            self.database = self.client.get_database(
                settings.astra_db_api_endpoint,
                keyspace=settings.astra_db_keyspace
            )
            
            # Get or create collection
            self.collection = self.database.get_collection(settings.collection_name)
            
            # If collection doesn't exist, create it
            if self.collection is None:
                self.collection = self.database.create_collection(
                    settings.collection_name
                )
            
            self._connected = True
            logger.info(f"Successfully connected to AstraDB collection: {settings.collection_name}")
            return True
            
        except DataAPIException as e:
            logger.error(f"Failed to connect to AstraDB: {str(e)}")
            self._connected = False
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to AstraDB: {str(e)}")
            self._connected = False
            return False
    
    def is_connected(self) -> bool:
        """Check if client is connected to AstraDB."""
        return self._connected
    
    async def create_item(self, item_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new item in the collection.
        
        Args:
            item_data: Dictionary containing item data
            
        Returns:
            Created item with ID and timestamps, or None if failed
        """
        try:
            # Add timestamps
            now = datetime.utcnow()
            document = {
                **item_data,
                "created_at": now,
                "updated_at": now
            }
            
            # Insert document
            result = self.collection.insert_one(document)
            
            # Return the created document with ID
            document["id"] = str(result.inserted_id)
            return document
            
        except DataAPIException as e:
            logger.error(f"Failed to create item: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating item: {str(e)}")
            return None
    
    async def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Item data or None if not found
        """
        try:
            result = self.collection.find_one({"_id": item_id})
            
            if result:
                result["id"] = str(result.pop("_id"))
                return result
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to get item {item_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting item {item_id}: {str(e)}")
            return None
    
    async def list_items(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all items with pagination.
        
        Args:
            skip: Number of items to skip
            limit: Maximum number of items to return
            
        Returns:
            List of items
        """
        try:
            cursor = self.collection.find({}, skip=skip, limit=limit)
            items = []
            
            for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                items.append(doc)
            
            return items
            
        except DataAPIException as e:
            logger.error(f"Failed to list items: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing items: {str(e)}")
            return []
    
    async def update_item(self, item_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an item by ID.
        
        Args:
            item_id: ID of the item to update
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated item or None if not found
        """
        try:
            # Add updated timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Update document
            result = self.collection.find_one_and_update(
                {"_id": item_id},
                {"$set": update_data},
                return_document="after"
            )
            
            if result:
                result["id"] = str(result.pop("_id"))
                return result
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to update item {item_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error updating item {item_id}: {str(e)}")
            return None
    
    async def delete_item(self, item_id: str) -> bool:
        """
        Delete an item by ID.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            result = self.collection.delete_one({"_id": item_id})
            return result.deleted_count > 0
            
        except DataAPIException as e:
            logger.error(f"Failed to delete item {item_id}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting item {item_id}: {str(e)}")
            return False
    
    async def count_items(self) -> int:
        """
        Count total number of items in the collection.
        
        Returns:
            Total count of items
        """
        try:
            return self.collection.count_documents({})
        except DataAPIException as e:
            logger.error(f"Failed to count items: {str(e)}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error counting items: {str(e)}")
            return 0


# Global database client instance
db_client = AstraDBClient()

# Made with Bob
