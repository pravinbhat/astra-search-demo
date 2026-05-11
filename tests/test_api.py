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


class TestMovieReviewsEndpoint:
    """Tests for movie_review CRUD endpoints."""
    
    def test_list_movie_reviews_empty(self):
        """Test listing movie_review documents returns the expected shape."""
        response = client.get("/api/movie-reviews")
        assert response.status_code == 200
        
        data = response.json()
        assert "movie_reviews" in data
        assert "total" in data
        assert isinstance(data["movie_reviews"], list)
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_create_movie_review(self):
        """Test creating a new movie_review document."""
        movie_review_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "creationdate": "2024-01-01T12:00:00Z",
            "criticname": "Test Critic",
            "originalscore": "4/5",
            "reviewstate": "published",
            "$vectorize": "A thoughtful and well-acted film."
        }
        
        response = client.post("/api/movie-reviews", json=movie_review_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == movie_review_data["title"]
        assert data["reviewid"] == movie_review_data["reviewid"]
        assert data["criticname"] == movie_review_data["criticname"]
        assert data["$vectorize"] == movie_review_data["$vectorize"]
        assert "id" in data
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_get_movie_review(self):
        """Test retrieving a specific movie_review document."""
        movie_review_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "This is a test review."
        }
        create_response = client.post("/api/movie-reviews", json=movie_review_data)
        movie_review_id = create_response.json()["id"]
        
        response = client.get(f"/api/movie-reviews/{movie_review_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == movie_review_id
        assert data["title"] == movie_review_data["title"]
        assert data["reviewid"] == movie_review_data["reviewid"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_update_movie_review(self):
        """Test updating a movie_review document."""
        movie_review_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "Original review text."
        }
        create_response = client.post("/api/movie-reviews", json=movie_review_data)
        movie_review_id = create_response.json()["id"]
        
        update_data = {
            "reviewstate": "approved",
            "$vectorize": "Updated review text."
        }
        response = client.put(f"/api/movie-reviews/{movie_review_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["reviewstate"] == update_data["reviewstate"]
        assert data["$vectorize"] == update_data["$vectorize"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_delete_movie_review(self):
        """Test deleting a movie_review document."""
        movie_review_data = {
            "title": "Test Movie",
            "reviewid": "review-123",
            "$vectorize": "To be deleted."
        }
        create_response = client.post("/api/movie-reviews", json=movie_review_data)
        movie_review_id = create_response.json()["id"]
        
        response = client.delete(f"/api/movie-reviews/{movie_review_id}")
        assert response.status_code == 204
        
        get_response = client.get(f"/api/movie-reviews/{movie_review_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_movie_review(self):
        """Test retrieving a non-existent movie_review document returns 404."""
        response = client.get("/api/movie-reviews/nonexistent-id")
        assert response.status_code == 404

# Made with Bob
