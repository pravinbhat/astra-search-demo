"""
Health check endpoint.
"""

from fastapi import APIRouter, status

from app.models import HealthResponse
from app.config import settings
from app.database import astra_connection_manager

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check the health status of the application and AstraDB connection"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify application and database status.
    
    Returns:
        HealthResponse: Application health status including AstraDB connection
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        astra_db_connected=astra_connection_manager.is_connected()
    )

# Made with Bob
