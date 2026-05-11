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


class TestMoviesEndpoint:
    """Tests for movie review CRUD endpoints."""
    
    def test_list_movies_empty(self):
        """Test listing movie review documents returns the expected shape."""
        response = client.get("/api/movies")
        assert response.status_code == 200
        
        data = response.json()
        assert "movies" in data
        assert "total" in data
        assert isinstance(data["movies"], list)
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_create_movie(self):
        """Test creating a new movie review document."""
        movie_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "creationdate": "2024-01-01T12:00:00Z",
            "criticname": "Test Critic",
            "originalscore": "4/5",
            "reviewstate": "published",
            "$vectorize": "A thoughtful and well-acted film."
        }
        
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == movie_data["title"]
        assert data["reviewid"] == movie_data["reviewid"]
        assert data["criticname"] == movie_data["criticname"]
        assert data["$vectorize"] == movie_data["$vectorize"]
        assert "id" in data
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_get_movie(self):
        """Test retrieving a specific movie review document."""
        movie_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "This is a test review."
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        response = client.get(f"/api/movies/{movie_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == movie_id
        assert data["title"] == movie_data["title"]
        assert data["reviewid"] == movie_data["reviewid"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_update_movie(self):
        """Test updating a movie review document."""
        movie_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "Original review text."
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        update_data = {
            "reviewstate": "approved",
            "$vectorize": "Updated review text."
        }
        response = client.put(f"/api/movies/{movie_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["reviewstate"] == update_data["reviewstate"]
        assert data["$vectorize"] == update_data["$vectorize"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_delete_movie(self):
        """Test deleting a movie review document."""
        movie_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "To be deleted."
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        response = client.delete(f"/api/movies/{movie_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/api/movies/{movie_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_movie(self):
        """Test retrieving a non-existent movie review document returns 404."""
        response = client.get("/api/movies/nonexistent-id")
        assert response.status_code == 404

# Made with Bob
