"""
FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import astra_connection_manager, library_book_repository
from app.routers import books, health

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting up application...")

    # Connect to AstraDB and initialize the application collection explicitly
    if astra_connection_manager.connect():
        collection = astra_connection_manager.ensure_collection(settings.collection_name)
        library_book_repository.set_collection(collection)
        logger.info(f"Successfully initialized AstraDB collection: {settings.collection_name}")
    else:
        logger.error("Failed to connect to AstraDB")

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A simple FastAPI application with AstraDB Data API for library book CRUD operations",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(books.router)

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"Mounted static files from {static_dir}")


@app.get("/", include_in_schema=False)
async def root():
    """
    Serve the UI.
    """
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    return {"error": "UI not found", "message": "Please check app/static/index.html"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)

# Made with Bob
