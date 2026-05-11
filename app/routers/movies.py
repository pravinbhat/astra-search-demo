"""
CRUD endpoints for movie review documents.
"""

from fastapi import APIRouter, HTTPException, status, Query

from app.models import (
    MovieReviewCreate,
    MovieReviewUpdate,
    MovieReviewResponse,
    MovieReviewListResponse,
    ErrorResponse
)
from app.database import db_client

router = APIRouter(prefix="/api/movie-reviews", tags=["Movie Reviews"])


@router.post(
    "",
    response_model=MovieReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Movie Review",
    description="Create a new movie review document in the database",
    responses={
        201: {"description": "Movie created successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_movie_review(movie_review: MovieReviewCreate) -> MovieReviewResponse:
    """
    Create a new movie review document.
    
    Args:
        movie_review: Movie review data to create
        
    Returns:
        Created movie review document
        
    Raises:
        HTTPException: If movie creation fails
    """
    movie_review_data = movie_review.model_dump(by_alias=True, exclude_none=True)
    result = await db_client.create_movie_review(movie_review_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create movie"
        )
    
    return MovieReviewResponse(**result)


@router.get(
    "",
    response_model=MovieReviewListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Movie Reviews",
    description="Retrieve a list of movie review documents with pagination"
)
async def list_movie_reviews(
    skip: int = Query(0, ge=0, description="Number of movie review documents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of movie review documents to return")
) -> MovieReviewListResponse:
    """
    List movie review documents with pagination.
    
    Args:
        skip: Number of movies to skip (for pagination)
        limit: Maximum number of movies to return
        
    Returns:
        List of movie review documents with total count
    """
    movie_reviews = await db_client.list_movie_reviews(skip=skip, limit=limit)
    total = await db_client.count_movie_reviews()
    
    return MovieReviewListResponse(
        movie_reviews=[MovieReviewResponse(**movie_review) for movie_review in movie_reviews],
        total=total
    )


@router.get(
    "/{movie_review_id}",
    response_model=MovieReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Movie Review",
    description="Retrieve a specific movie review document by ID",
    responses={
        200: {"description": "Movie found"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def get_movie_review(movie_review_id: str) -> MovieReviewResponse:
    """
    Get a specific movie review document by ID.
    
    Args:
        movie_review_id: ID of the movie review to retrieve
        
    Returns:
        Movie review document data
        
    Raises:
        HTTPException: If movie not found
    """
    result = await db_client.get_movie_review(movie_review_id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie review with ID {movie_review_id} not found"
        )
    
    return MovieReviewResponse(**result)


@router.put(
    "/{movie_id}",
    response_model=MovieReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Movie Review",
    description="Update an existing movie review document by ID",
    responses={
        200: {"description": "Movie updated successfully"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def update_movie_review(movie_review_id: str, movie_review: MovieReviewUpdate) -> MovieReviewResponse:
    """
    Update an existing movie review document.
    
    Args:
        movie_review_id: ID of the movie review to update
        movie_review: Updated movie review data
        
    Returns:
        Updated movie review document data
        
    Raises:
        HTTPException: If movie not found
    """
    update_data = movie_review.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = await db_client.update_movie_review(movie_review_id, update_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie review with ID {movie_review_id} not found"
        )
    
    return MovieReviewResponse(**result)


@router.delete(
    "/{movie_review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Movie Review",
    description="Delete a movie review document by ID",
    responses={
        204: {"description": "Movie deleted successfully"},
        404: {"model": ErrorResponse, "description": "Movie not found"}
    }
)
async def delete_movie_review(movie_review_id: str) -> None:
    """
    Delete a movie review document by ID.
    
    Args:
        movie_review_id: ID of the movie review to delete
        
    Raises:
        HTTPException: If movie not found
    """
    success = await db_client.delete_movie_review(movie_review_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie review with ID {movie_review_id} not found"
        )

# Made with Bob
