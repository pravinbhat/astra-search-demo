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
    
    def _ensure_collection(self):
        """Return the active collection or raise if not connected."""
        if self.collection is None:
            raise RuntimeError("AstraDB collection is not initialized")
        return self.collection

    def _normalize_library_book_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Map Astra document fields to API response fields."""
        normalized = dict(doc)
        normalized["id"] = str(normalized.pop("_id"))
        
        # Convert DataAPITimestamp to string if present
        if "due_date" in normalized and normalized["due_date"] is not None:
            # Check if it's a DataAPITimestamp object
            if hasattr(normalized["due_date"], "to_string"):
                normalized["due_date"] = normalized["due_date"].to_string()
            elif hasattr(normalized["due_date"], "isoformat"):
                normalized["due_date"] = normalized["due_date"].isoformat()
        
        return normalized

    async def create_library_book(self, library_book_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new library book document in the collection.
        
        Args:
            library_book_data: Dictionary containing library book data
            
        Returns:
            Created library book document, or None if failed
        """
        try:
            collection = self._ensure_collection()
            document = dict(library_book_data)
            result = collection.insert_one(document)

            created = collection.find_one({"_id": result.inserted_id})
            if created:
                return self._normalize_library_book_document(created)

            document["_id"] = result.inserted_id
            return self._normalize_library_book_document(document)
            
        except DataAPIException as e:
            logger.error(f"Failed to create library book: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating library book: {str(e)}")
            return None
    
    async def get_library_book(self, library_book_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a library book document by ID.
        
        Args:
            library_book_id: ID of the library book to retrieve
            
        Returns:
            Library book data or None if not found
        """
        try:
            collection = self._ensure_collection()
            result = collection.find_one({"_id": library_book_id})
            
            if result:
                return self._normalize_library_book_document(result)
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to get library book {library_book_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting library book {library_book_id}: {str(e)}")
            return None
    
    async def list_library_books(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List library book documents with pagination.
        
        Args:
            skip: Number of library book documents to skip
            limit: Maximum number of library book documents to return
            
        Returns:
            List of library book documents
        """
        try:
            collection = self._ensure_collection()
            cursor = collection.find({}, limit=skip + limit)
            library_books = []
            
            for index, doc in enumerate(cursor):
                if index < skip:
                    continue
                library_books.append(self._normalize_library_book_document(doc))
                if len(library_books) >= limit:
                    break
            
            return library_books
            
        except DataAPIException as e:
            logger.error(f"Failed to list library books: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing library books: {str(e)}")
            return []
    
    async def update_library_book(self, library_book_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a library book document by ID.
        
        Args:
            library_book_id: ID of the library book to update
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated library book document or None if not found
        """
        try:
            collection = self._ensure_collection()
            result = collection.find_one_and_update(
                {"_id": library_book_id},
                {"$set": update_data},
                return_document="after"
            )
            
            if result:
                return self._normalize_library_book_document(result)
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to update library book {library_book_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error updating library book {library_book_id}: {str(e)}")
            return None
    
    async def delete_library_book(self, library_book_id: str) -> bool:
        """
        Delete a library book document by ID.
        
        Args:
            library_book_id: ID of the library book to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            collection = self._ensure_collection()
            result = collection.delete_one({"_id": library_book_id})
            return result.deleted_count > 0
            
        except DataAPIException as e:
            logger.error(f"Failed to delete library book {library_book_id}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting library book {library_book_id}: {str(e)}")
            return False
    
    async def count_library_books(self) -> int:
        """
        Count total number of library book documents in the collection.
        
        Returns:
            Total count of library book documents
        """
        try:
            collection = self._ensure_collection()
            return collection.count_documents({}, upper_bound=1000000)
        except DataAPIException as e:
            logger.error(f"Failed to count library books: {str(e)}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error counting library books: {str(e)}")
            return 0
    
    async def search_library_books(
        self,
        filter_predicates: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Dict[str, Any]], int]:
        """
        Search library book documents using filter predicates.
        
        Args:
            filter_predicates: Dictionary containing filter predicates for the search
                              (e.g., {'author': 'John Anthony', 'rating': {'$gte': 4.0}})
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            Tuple of (list of matching library book documents, total count of matches)
            
        Examples:
            # Simple equality filter
            await search_library_books({'author': 'John Anthony'})
            
            # Range filter
            await search_library_books({'rating': {'$gte': 4.0}})
            
            # Multiple conditions
            await search_library_books({'author': 'John Anthony', 'is_checked_out': False})
            
            # Array contains filter
            await search_library_books({'genres': {'$in': ['Science Fiction', 'Fantasy']}})
        """
        try:
            collection = self._ensure_collection()
            
            # Count total matching documents
            total = collection.count_documents(filter_predicates, upper_bound=1000000)
            
            # Find documents with pagination
            cursor = collection.find(filter_predicates, limit=skip + limit)
            library_books = []
            
            for index, doc in enumerate(cursor):
                if index < skip:
                    continue
                library_books.append(self._normalize_library_book_document(doc))
                if len(library_books) >= limit:
                    break
            
            logger.info(f"Search completed: found {total} documents, returning {len(library_books)}")
            return library_books, total
            
        except DataAPIException as e:
            logger.error(f"Failed to search library books: {str(e)}")
            return [], 0
        except Exception as e:
            logger.error(f"Unexpected error searching library books: {str(e)}")
            return [], 0


# Global database client instance
db_client = AstraDBClient()

# Made with Bob
