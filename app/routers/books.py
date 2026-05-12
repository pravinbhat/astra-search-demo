"""
CRUD endpoints for library book documents.
"""

from fastapi import APIRouter, HTTPException, status, Query

from app.models import (
    LibraryBookCreate,
    LibraryBookUpdate,
    LibraryBookResponse,
    LibraryBookListResponse,
    LibraryBookSearchRequest,
    ErrorResponse
)
from app.database import db_client

router = APIRouter(prefix="/api/library-books", tags=["Library Books"])


@router.post(
    "",
    response_model=LibraryBookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Library Book",
    description="Create a new library book document in the database",
    responses={
        201: {"description": "Library book created successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_library_book(library_book: LibraryBookCreate) -> LibraryBookResponse:
    """
    Create a new library book document.
    
    Args:
        library_book: Library book data to create
        
    Returns:
        Created library book document
        
    Raises:
        HTTPException: If library book creation fails
    """
    library_book_data = library_book.model_dump(by_alias=True, exclude_none=True)
    result = await db_client.create_library_book(library_book_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create library book"
        )
    
    return LibraryBookResponse(**result)


@router.get(
    "",
    response_model=LibraryBookListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Library Books",
    description="Retrieve a list of library book documents with pagination"
)
async def list_library_books(
    skip: int = Query(0, ge=0, description="Number of library book documents to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of library book documents to return")
) -> LibraryBookListResponse:
    """
    List library book documents with pagination.
    
    Args:
        skip: Number of books to skip (for pagination)
        limit: Maximum number of books to return
        
    Returns:
        List of library book documents with total count
    """
    library_books = await db_client.list_library_books(skip=skip, limit=limit)
    total = await db_client.count_library_books()
    
    return LibraryBookListResponse(
        library_books=[LibraryBookResponse(**library_book) for library_book in library_books],
        total=total
    )


@router.post(
    "/search",
    response_model=LibraryBookListResponse,
    status_code=status.HTTP_200_OK,
    summary="Search Library Books",
    description="Search library book documents using filters, semantic queries, or both",
    responses={
        200: {"description": "Search completed successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def search_library_books(search_filter: LibraryBookSearchRequest) -> LibraryBookListResponse:
    """
    Search library book documents using filters, semantic queries, or both.
    
    Supported search modes:
    - Filter search: {"filter": {"author": "John Anthony"}}
    - Semantic search: {"query": "books about resilience and survival"}
    - Semantic filter search: {"filter": {"genres": {"$in": ["Science Fiction"]}}, "query": "books about space exploration"}
    
    Args:
        search_filter: Search request containing filter predicates, optional semantic query, skip, and limit
        
    Returns:
        List of matching library book documents with total count
        
    Raises:
        HTTPException: If search fails
        
    Examples:
        # Filter search by author
        {"filter": {"author": "John Anthony"}, "skip": 0, "limit": 10}
        
        # Semantic search by query
        {"query": "books about resilience and survival", "skip": 0, "limit": 10}
        
        # Semantic filter search
        {"filter": {"genres": {"$in": ["Science Fiction", "Fantasy"]}}, "query": "books about space exploration", "skip": 0, "limit": 20}
    """
    try:
        query = search_filter.query.strip() if search_filter.query else None
        if query:
            library_books, total = await db_client.semantic_search_library_books(
                query=query,
                filter_predicates=search_filter.filter,
                skip=search_filter.skip,
                limit=search_filter.limit
            )
        else:
            library_books, total = await db_client.search_library_books(
                filter_predicates=search_filter.filter,
                skip=search_filter.skip,
                limit=search_filter.limit
            )
        
        return LibraryBookListResponse(
            library_books=[LibraryBookResponse(**library_book) for library_book in library_books],
            total=total
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get(
    "/{library_book_id}",
    response_model=LibraryBookResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Library Book",
    description="Retrieve a specific library book document by ID",
    responses={
        200: {"description": "Library book found"},
        404: {"model": ErrorResponse, "description": "Library book not found"}
    }
)
async def get_library_book(library_book_id: str) -> LibraryBookResponse:
    """
    Get a specific library book document by ID.
    
    Args:
        library_book_id: ID of the library book to retrieve
        
    Returns:
        Library book document data
        
    Raises:
        HTTPException: If library book not found
    """
    result = await db_client.get_library_book(library_book_id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library book with ID {library_book_id} not found"
        )
    
    return LibraryBookResponse(**result)


@router.put(
    "/{library_book_id}",
    response_model=LibraryBookResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Library Book",
    description="Update an existing library book document by ID",
    responses={
        200: {"description": "Library book updated successfully"},
        404: {"model": ErrorResponse, "description": "Library book not found"}
    }
)
async def update_library_book(library_book_id: str, library_book: LibraryBookUpdate) -> LibraryBookResponse:
    """
    Update an existing library book document.
    
    Args:
        library_book_id: ID of the library book to update
        library_book: Updated library book data
        
    Returns:
        Updated library book document data
        
    Raises:
        HTTPException: If library book not found
    """
    update_data = library_book.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = await db_client.update_library_book(library_book_id, update_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library book with ID {library_book_id} not found"
        )
    
    return LibraryBookResponse(**result)


@router.delete(
    "/{library_book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Library Book",
    description="Delete a library book document by ID",
    responses={
        204: {"description": "Library book deleted successfully"},
        404: {"model": ErrorResponse, "description": "Library book not found"}
    }
)
async def delete_library_book(library_book_id: str) -> None:
    """
    Delete a library book document by ID.
    
    Args:
        library_book_id: ID of the library book to delete
        
    Raises:
        HTTPException: If library book not found
    """
    success = await db_client.delete_library_book(library_book_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library book with ID {library_book_id} not found"
        )

# Made with Bob