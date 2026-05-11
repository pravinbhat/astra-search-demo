"""
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    """Base schema for Movie."""
    name: str = Field(..., description="Name of the movie", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description of the movie", max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class MovieCreate(MovieBase):
    """Schema for creating a new movie."""
    pass


class MovieUpdate(BaseModel):
    """Schema for updating a movie. All fields are optional."""
    name: Optional[str] = Field(None, description="Name of the movie", min_length=1, max_length=100)
    description: Optional[str] = Field(None, description="Description of the movie", max_length=500)
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class MovieResponse(MovieBase):
    """Schema for movie response."""
    id: str = Field(..., description="Unique identifier for the movie")
    created_at: datetime = Field(..., description="Timestamp when the movie was created")
    updated_at: datetime = Field(..., description="Timestamp when the movie was last updated")
    
    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    """Schema for list of movies response."""
    movies: list[MovieResponse] = Field(..., description="List of movies")
    total: int = Field(..., description="Total number of movies")


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
