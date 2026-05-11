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

    def _normalize_movie_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Map Astra document fields to API response fields."""
        normalized = dict(doc)
        normalized["id"] = str(normalized.pop("_id"))
        return normalized

    async def create_movie(self, movie_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new movie review document in the collection.
        
        Args:
            movie_data: Dictionary containing movie review data
            
        Returns:
            Created movie review document, or None if failed
        """
        try:
            collection = self._ensure_collection()
            document = dict(movie_data)
            result = collection.insert_one(document)

            created = collection.find_one({"_id": result.inserted_id})
            if created:
                return self._normalize_movie_document(created)

            document["_id"] = result.inserted_id
            return self._normalize_movie_document(document)
            
        except DataAPIException as e:
            logger.error(f"Failed to create movie: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating movie: {str(e)}")
            return None
    
    async def get_movie(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a movie review document by ID.
        
        Args:
            movie_id: ID of the movie review to retrieve
            
        Returns:
            Movie review data or None if not found
        """
        try:
            collection = self._ensure_collection()
            result = collection.find_one({"_id": movie_id})
            
            if result:
                return self._normalize_movie_document(result)
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to get movie {movie_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting movie {movie_id}: {str(e)}")
            return None
    
    async def list_movies(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List movie review documents with pagination.
        
        Args:
            skip: Number of movie review documents to skip
            limit: Maximum number of movie review documents to return
            
        Returns:
            List of movie review documents
        """
        try:
            collection = self._ensure_collection()
            cursor = collection.find({}, limit=skip + limit)
            movies = []
            
            for index, doc in enumerate(cursor):
                if index < skip:
                    continue
                movies.append(self._normalize_movie_document(doc))
                if len(movies) >= limit:
                    break
            
            return movies
            
        except DataAPIException as e:
            logger.error(f"Failed to list movies: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing movies: {str(e)}")
            return []
    
    async def update_movie(self, movie_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a movie review document by ID.
        
        Args:
            movie_id: ID of the movie review to update
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated movie review document or None if not found
        """
        try:
            collection = self._ensure_collection()
            result = collection.find_one_and_update(
                {"_id": movie_id},
                {"$set": update_data},
                return_document="after"
            )
            
            if result:
                return self._normalize_movie_document(result)
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to update movie {movie_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error updating movie {movie_id}: {str(e)}")
            return None
    
    async def delete_movie(self, movie_id: str) -> bool:
        """
        Delete a movie by ID.
        
        Args:
            movie_id: ID of the movie to delete
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            collection = self._ensure_collection()
            result = collection.delete_one({"_id": movie_id})
            return result.deleted_count > 0
            
        except DataAPIException as e:
            logger.error(f"Failed to delete movie {movie_id}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting movie {movie_id}: {str(e)}")
            return False
    
    async def count_movies(self) -> int:
        """
        Count total number of movies in the collection.
        
        Returns:
            Total count of movies
        """
        try:
            collection = self._ensure_collection()
            return collection.count_documents({}, upper_bound=1000000)
        except DataAPIException as e:
            logger.error(f"Failed to count movies: {str(e)}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error counting movies: {str(e)}")
            return 0


# Global database client instance
db_client = AstraDBClient()

# Made with Bob
