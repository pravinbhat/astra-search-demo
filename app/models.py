"""
Pydantic models for request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class MovieBase(BaseModel):
    """Base schema for a movie review document."""
    title: str = Field(..., description="Movie title", min_length=1, max_length=300)
    reviewid: str = Field(..., description="External review identifier", min_length=1, max_length=100)
    creationdate: Optional[datetime] = Field(None, description="Review creation timestamp")
    criticname: Optional[str] = Field(None, description="Name of the critic", max_length=200)
    originalscore: Optional[str] = Field(None, description="Original score from the review source", max_length=100)
    reviewstate: Optional[str] = Field(None, description="Review state", max_length=100)
    vectorize_text: Optional[str] = Field(
        None,
        alias="$vectorize",
        description="Review text used by AstraDB to generate embeddings",
        min_length=1
    )

    model_config = ConfigDict(populate_by_name=True)


class MovieCreate(MovieBase):
    """Schema for creating a new movie review document."""
    pass


class MovieUpdate(BaseModel):
    """Schema for updating a movie review document. All fields are optional."""
    title: Optional[str] = Field(None, description="Movie title", min_length=1, max_length=300)
    reviewid: Optional[str] = Field(None, description="External review identifier", min_length=1, max_length=100)
    creationdate: Optional[datetime] = Field(None, description="Review creation timestamp")
    criticname: Optional[str] = Field(None, description="Name of the critic", max_length=200)
    originalscore: Optional[str] = Field(None, description="Original score from the review source", max_length=100)
    reviewstate: Optional[str] = Field(None, description="Review state", max_length=100)
    vectorize_text: Optional[str] = Field(
        None,
        alias="$vectorize",
        description="Review text used by AstraDB to generate embeddings",
        min_length=1
    )

    model_config = ConfigDict(populate_by_name=True)


class MovieResponse(MovieBase):
    """Schema for movie review response."""
    id: str = Field(..., description="Unique identifier for the movie review")
    embedding: Optional[list[float]] = Field(None, description="Optional embedding payload if stored in the document")
    vector: Optional[list[float]] = Field(None, alias="$vector", description="Stored Astra vector, if returned")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MovieListResponse(BaseModel):
    """Schema for list of movie review documents."""
    movies: list[MovieResponse] = Field(..., description="List of movie review documents")
    total: int = Field(..., description="Total number of movie review documents")


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
