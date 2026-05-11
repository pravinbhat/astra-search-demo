"""
CRUD endpoints for movies.
"""

from fastapi import APIRouter, HTTPException, status, Query

from app.models import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieListResponse,
    ErrorResponse
)
from app.database import db_client

router = APIRouter(prefix="/api/movies", tags=["Movies"])


@router.post(
    "",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Movie",
    description="Create a new movie in the database",
    responses={
        201: {"description": "Movie created successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_movie(movie: MovieCreate) -> MovieResponse:
    """
    Create a new movie.
    
    Args:
        movie: Movie data to create
        
    Returns:
        Created movie with ID and timestamps
        
    Raises:
        HTTPException: If movie creation fails
    """
    movie_data = movie.model_dump()
    result = await db_client.create_movie(movie_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create movie"
        )
    
    return MovieResponse(**result)


@router.get(
    "",
    response_model=MovieListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Movies",
    description="Retrieve a list of all movies with pagination"
)
async def list_movies(
    skip: int = Query(0, ge=0, description="Number of movies to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of movies to return")
) -> MovieListResponse:
    """
    List all movies with pagination.
    
    Args:
        skip: Number of movies to skip (for pagination)
        limit: Maximum number of movies to return
        
    Returns:
        List of movies with total count
    """
    movies = await db_client.list_movies(skip=skip, limit=limit)
    total = await db_client.count_movies()
    
    return MovieListResponse(
        movies=[MovieResponse(**movie) for movie in movies],
        total=total
    )


@router.get(
    "/{movie_id}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Movie",
    description="Retrieve a specific movie by ID",
    responses={
        200: {"description": "Movie found"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def get_movie(movie_id: str) -> MovieResponse:
    """
    Get a specific movie by ID.
    
    Args:
        movie_id: ID of the movie to retrieve
        
    Returns:
        Movie data
        
    Raises:
        HTTPException: If movie not found
    """
    result = await db_client.get_movie(movie_id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found"
        )
    
    return MovieResponse(**result)


@router.put(
    "/{movie_id}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Movie",
    description="Update an existing movie by ID",
    responses={
        200: {"description": "Movie updated successfully"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def update_movie(movie_id: str, movie: MovieUpdate) -> MovieResponse:
    """
    Update an existing movie.
    
    Args:
        movie_id: ID of the movie to update
        movie: Updated movie data
        
    Returns:
        Updated movie data
        
    Raises:
        HTTPException: If movie not found
    """
    update_data = movie.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = await db_client.update_movie(movie_id, update_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found"
        )
    
    return MovieResponse(**result)


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Movie",
    description="Delete a movie by ID",
    responses={
        204: {"description": "Movie deleted successfully"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def delete_movie(movie_id: str) -> None:
    """
    Delete a movie by ID.
    
    Args:
        movie_id: ID of the movie to delete
        
    Raises:
        HTTPException: If movie not found
    """
    success = await db_client.delete_movie(movie_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found"
        )

# Made with Bob
