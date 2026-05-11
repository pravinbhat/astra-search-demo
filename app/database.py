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
    
    async def create_movie(self, movie_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new movie in the collection.
        
        Args:
            movie_data: Dictionary containing movie data
            
        Returns:
            Created movie with ID and timestamps, or None if failed
        """
        try:
            now = datetime.utcnow()
            document = {
                **movie_data,
                "created_at": now,
                "updated_at": now
            }
            
            result = self.collection.insert_one(document)
            document["id"] = str(result.inserted_id)
            return document
            
        except DataAPIException as e:
            logger.error(f"Failed to create movie: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating movie: {str(e)}")
            return None
    
    async def get_movie(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a movie by ID.
        
        Args:
            movie_id: ID of the movie to retrieve
            
        Returns:
            Movie data or None if not found
        """
        try:
            result = self.collection.find_one({"_id": movie_id})
            
            if result:
                result["id"] = str(result.pop("_id"))
                return result
            return None
            
        except DataAPIException as e:
            logger.error(f"Failed to get movie {movie_id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting movie {movie_id}: {str(e)}")
            return None
    
    async def list_movies(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all movies with pagination.
        
        Args:
            skip: Number of movies to skip
            limit: Maximum number of movies to return
            
        Returns:
            List of movies
        """
        try:
            cursor = self.collection.find({}, limit=skip + limit)
            movies = []
            
            for index, doc in enumerate(cursor):
                if index < skip:
                    continue
                doc["id"] = str(doc.pop("_id"))
                movies.append(doc)
            
            return movies
            
        except DataAPIException as e:
            logger.error(f"Failed to list movies: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error listing movies: {str(e)}")
            return []
    
    async def update_movie(self, movie_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a movie by ID.
        
        Args:
            movie_id: ID of the movie to update
            update_data: Dictionary containing fields to update
            
        Returns:
            Updated movie or None if not found
        """
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = self.collection.find_one_and_update(
                {"_id": movie_id},
                {"$set": update_data},
                return_document="after"
            )
            
            if result:
                result["id"] = str(result.pop("_id"))
                return result
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
            result = self.collection.delete_one({"_id": movie_id})
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
            return self.collection.count_documents({}, upper_bound=1000000)
        except DataAPIException as e:
            logger.error(f"Failed to count movies: {str(e)}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error counting movies: {str(e)}")
            return 0


# Global database client instance
db_client = AstraDBClient()

# Made with Bob
