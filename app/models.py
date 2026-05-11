"""
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base schema for Item."""
    name: str = Field(..., description="Name of the item", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description of the item", max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item. All fields are optional."""
    name: Optional[str] = Field(None, description="Name of the item", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description of the item", max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ItemResponse(ItemBase):
    """Schema for item response."""
    id: str = Field(..., description="Unique identifier for the item")
    created_at: datetime = Field(..., description="Timestamp when the item was created")
    updated_at: datetime = Field(..., description="Timestamp when the item was last updated")
    
    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    """Schema for list of items response."""
    items: list[ItemResponse] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Health status")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
    astra_db_connected: bool = Field(..., description="AstraDB connection status")


class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str = Field(..., description="Error message")

# Made with Bob
