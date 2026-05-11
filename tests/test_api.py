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
    """Tests for movies CRUD endpoints."""
    
    def test_list_movies_empty(self):
        """Test listing movies returns empty list initially."""
        response = client.get("/api/movies")
        assert response.status_code == 200
        
        data = response.json()
        assert "movies" in data
        assert "total" in data
        assert isinstance(data["movies"], list)
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_create_movie(self):
        """Test creating a new movie."""
        movie_data = {
            "name": "Test Movie",
            "description": "This is a test movie",
            "metadata": {"category": "test"}
        }
        
        response = client.post("/api/movies", json=movie_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == movie_data["name"]
        assert data["description"] == movie_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_get_movie(self):
        """Test retrieving a specific movie."""
        movie_data = {
            "name": "Test Movie",
            "description": "This is a test movie"
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        response = client.get(f"/api/movies/{movie_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == movie_id
        assert data["name"] == movie_data["name"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_update_movie(self):
        """Test updating a movie."""
        movie_data = {
            "name": "Test Movie",
            "description": "Original description"
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        update_data = {
            "description": "Updated description"
        }
        response = client.put(f"/api/movies/{movie_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["description"] == update_data["description"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_delete_movie(self):
        """Test deleting a movie."""
        movie_data = {
            "name": "Test Movie",
            "description": "To be deleted"
        }
        create_response = client.post("/api/movies", json=movie_data)
        movie_id = create_response.json()["id"]
        
        response = client.delete(f"/api/movies/{movie_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/api/movies/{movie_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_movie(self):
        """Test retrieving a non-existent movie returns 404."""
        response = client.get("/api/movies/nonexistent-id")
        assert response.status_code == 404

# Made with Bob
