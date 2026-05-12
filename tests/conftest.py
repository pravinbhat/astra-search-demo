"""
Pytest configuration and shared fixtures for tests.
"""

import pytest
from app.config import settings
from app.database import astra_connection_manager, library_book_repository


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Setup database connection for all tests.
    This fixture runs once per test session and ensures the database is connected.
    The database credentials are loaded from the .env file via app.config.settings.
    """
    # Connect to the database using credentials from .env file
    if not astra_connection_manager.is_connected():
        success = astra_connection_manager.connect()
        if not success:
            pytest.fail(
                "Failed to connect to AstraDB. "
                "Please ensure your .env file exists and contains valid credentials:\n"
                "  - ASTRA_DB_API_ENDPOINT\n"
                "  - ASTRA_DB_APPLICATION_TOKEN\n"
                "  - ASTRA_DB_KEYSPACE\n"
                "  - COLLECTION_NAME"
            )

        collection = astra_connection_manager.ensure_collection(settings.collection_name)
        library_book_repository.set_collection(collection)
    
    yield
    
    # Cleanup after all tests (optional)
    # You can add session-level cleanup logic here if needed


@pytest.fixture
async def cleanup_test_books():
    """
    Fixture to clean up test books created during tests.
    Yields a list to track book IDs, then deletes them after the test.
    
    Usage:
        async def test_something(cleanup_test_books):
            # Create a book
            response = client.post("/api/library-books", json=book_data)
            book_id = response.json()["id"]
            
            # Track it for cleanup
            cleanup_test_books.append(book_id)
            
            # Test continues...
            # Book will be automatically deleted after test completes
    """
    created_book_ids = []
    
    yield created_book_ids
    
    # Cleanup: delete all books created during the test
    for book_id in created_book_ids:
        try:
            await library_book_repository.delete_library_book(book_id)
        except Exception as e:
            print(f"Warning: Failed to cleanup book {book_id}: {e}")


# Made with Bob