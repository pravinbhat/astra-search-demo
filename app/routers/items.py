"""
CRUD endpoints for items.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status, Query

from app.models import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemListResponse,
    ErrorResponse
)
from app.database import db_client

router = APIRouter(prefix="/api/items", tags=["Items"])


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Item",
    description="Create a new item in the database",
    responses={
        201: {"description": "Item created successfully"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def create_item(item: ItemCreate) -> ItemResponse:
    """
    Create a new item.
    
    Args:
        item: Item data to create
        
    Returns:
        Created item with ID and timestamps
        
    Raises:
        HTTPException: If item creation fails
    """
    item_data = item.model_dump()
    result = await db_client.create_item(item_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )
    
    return ItemResponse(**result)


@router.get(
    "",
    response_model=ItemListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Items",
    description="Retrieve a list of all items with pagination"
)
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return")
) -> ItemListResponse:
    """
    List all items with pagination.
    
    Args:
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        
    Returns:
        List of items with total count
    """
    items = await db_client.list_items(skip=skip, limit=limit)
    total = await db_client.count_items()
    
    return ItemListResponse(
        items=[ItemResponse(**item) for item in items],
        total=total
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Item",
    description="Retrieve a specific item by ID",
    responses={
        200: {"description": "Item found"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    }
)
async def get_item(item_id: str) -> ItemResponse:
    """
    Get a specific item by ID.
    
    Args:
        item_id: ID of the item to retrieve
        
    Returns:
        Item data
        
    Raises:
        HTTPException: If item not found
    """
    result = await db_client.get_item(item_id)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return ItemResponse(**result)


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Item",
    description="Update an existing item by ID",
    responses={
        200: {"description": "Item updated successfully"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    }
)
async def update_item(item_id: str, item: ItemUpdate) -> ItemResponse:
    """
    Update an existing item.
    
    Args:
        item_id: ID of the item to update
        item: Updated item data
        
    Returns:
        Updated item data
        
    Raises:
        HTTPException: If item not found
    """
    # Only include fields that were actually set
    update_data = item.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    result = await db_client.update_item(item_id, update_data)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return ItemResponse(**result)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Item",
    description="Delete an item by ID",
    responses={
        204: {"description": "Item deleted successfully"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    }
)
async def delete_item(item_id: str) -> None:
    """
    Delete an item by ID.
    
    Args:
        item_id: ID of the item to delete
        
    Raises:
        HTTPException: If item not found
    """
    success = await db_client.delete_item(item_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

# Made with Bob
