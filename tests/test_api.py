"""
Basic API tests for the FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "app_name" in data
        assert "version" in data
        assert "astra_db_connected" in data


class TestRootEndpoint:
    """Tests for root endpoint."""
    
    def test_root(self):
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data


class TestLibraryBooksEndpoint:
    """Tests for library_book CRUD endpoints."""
    
    def test_list_library_books_empty(self):
        """Test listing library_book documents returns the expected shape (limited to top 5)."""
        response = client.get("/api/library-books?limit=5")
        assert response.status_code == 200
        
        data = response.json()

        assert "library_books" in data
        assert "total" in data
        assert isinstance(data["library_books"], list)
        assert len(data["library_books"]) <= 5, "Should return at most 5 books"
    
    @pytest.mark.asyncio
    async def test_create_library_book(self, cleanup_test_books):
        """Test creating a new library_book document."""
        library_book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "number_of_pages": 300,
            "rating": 4.5,
            "publication_year": 2024,
            "summary": "A test book for unit testing.",
            "genres": ["Fiction", "Test"],
            "metadata": {
                "isbn": "978-0-123456-78-9",
                "language": "English",
                "edition": "First Edition"
            },
            "is_checked_out": False,
            "borrower": None,
            "due_date": None,
            "$vectorize": "summary: A test book for unit testing. | genres: Fiction, Test"
        }
        
        response = client.post("/api/library-books", json=library_book_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == library_book_data["title"]
        assert data["author"] == library_book_data["author"]
        assert data["number_of_pages"] == library_book_data["number_of_pages"]
        assert data["rating"] == library_book_data["rating"]
        assert "id" in data
        
        # Track for cleanup
        cleanup_test_books.append(data["id"])
    
    @pytest.mark.asyncio
    async def test_get_library_book(self, cleanup_test_books):
        """Test retrieving a specific library_book document."""
        library_book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "number_of_pages": 300,
            "rating": 4.5,
            "publication_year": 2024,
            "summary": "A test book.",
            "genres": ["Fiction"],
            "metadata": {
                "isbn": "978-0-123456-78-9",
                "language": "English",
                "edition": "First Edition"
            },
            "is_checked_out": False,
            "borrower": None,
            "due_date": None,
            "$vectorize": "summary: A test book. | genres: Fiction"
        }
        create_response = client.post("/api/library-books", json=library_book_data)
        library_book_id = create_response.json()["id"]
        cleanup_test_books.append(library_book_id)
        
        response = client.get(f"/api/library-books/{library_book_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == library_book_id
        assert data["title"] == library_book_data["title"]
        assert data["author"] == library_book_data["author"]
    
    @pytest.mark.asyncio
    async def test_update_library_book(self, cleanup_test_books):
        """Test updating a library_book document."""
        library_book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "number_of_pages": 300,
            "rating": 4.5,
            "publication_year": 2024,
            "summary": "Original summary.",
            "genres": ["Fiction"],
            "metadata": {
                "isbn": "978-0-123456-78-9",
                "language": "English",
                "edition": "First Edition"
            },
            "is_checked_out": False,
            "borrower": None,
            "due_date": None,
            "$vectorize": "summary: Original summary. | genres: Fiction"
        }
        create_response = client.post("/api/library-books", json=library_book_data)
        library_book_id = create_response.json()["id"]
        cleanup_test_books.append(library_book_id)
        
        update_data = {
            "is_checked_out": True,
            "borrower": "John Doe",
            "due_date": "2024-12-31T23:59:59Z"
        }
        response = client.put(f"/api/library-books/{library_book_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_checked_out"] == update_data["is_checked_out"]
        assert data["borrower"] == update_data["borrower"]
    
    @pytest.mark.asyncio
    async def test_delete_library_book(self, cleanup_test_books):
        """Test deleting a library_book document."""
        library_book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "number_of_pages": 300,
            "rating": 4.5,
            "publication_year": 2024,
            "summary": "To be deleted.",
            "genres": ["Fiction"],
            "metadata": {
                "isbn": "978-0-123456-78-9",
                "language": "English",
                "edition": "First Edition"
            },
            "is_checked_out": False,
            "borrower": None,
            "due_date": None,
            "$vectorize": "summary: To be deleted. | genres: Fiction"
        }
        create_response = client.post("/api/library-books", json=library_book_data)
        library_book_id = create_response.json()["id"]
        # Note: No need to track for cleanup since we're testing deletion
        
        response = client.delete(f"/api/library-books/{library_book_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/api/library-books/{library_book_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_library_book(self):
        """Test retrieving a non-existent library_book document returns 404."""
        response = client.get("/api/library-books/nonexistent-id")
        assert response.status_code == 404

    def test_search_library_books_with_filter(self):
        """Test filter search returns the expected response shape."""
        response = client.post(
            "/api/library-books/search",
            json={
                "filter": {"author": "John Anthony"},
                "skip": 0,
                "limit": 5,
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "library_books" in data
        assert "total" in data
        assert isinstance(data["library_books"], list)

    def test_search_library_books_with_query(self):
        """Test semantic search request is accepted and returns similarity metadata when available."""
        response = client.post(
            "/api/library-books/search",
            json={
                "query": "books about resilience and survival",
                "skip": 0,
                "limit": 5,
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "library_books" in data
        assert "total" in data
        assert isinstance(data["library_books"], list)

        for book in data["library_books"]:
            assert "$similarity" in book or book.get("$similarity") is None

    def test_search_library_books_with_filter_and_query(self):
        """Test semantic filter search request is accepted and returns the expected response shape."""
        response = client.post(
            "/api/library-books/search",
            json={
                "filter": {"genres": {"$in": ["Science Fiction"]}},
                "query": "books about futuristic worlds",
                "skip": 0,
                "limit": 5,
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert "library_books" in data
        assert "total" in data
        assert isinstance(data["library_books"], list)

# Made with Bob
