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


class TestItemsEndpoint:
    """Tests for items CRUD endpoints."""
    
    def test_list_items_empty(self):
        """Test listing items returns empty list initially."""
        response = client.get("/api/items")
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_create_item(self):
        """Test creating a new item."""
        item_data = {
            "name": "Test Item",
            "description": "This is a test item",
            "metadata": {"category": "test"}
        }
        
        response = client.post("/api/items", json=item_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == item_data["name"]
        assert data["description"] == item_data["description"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_get_item(self):
        """Test retrieving a specific item."""
        # First create an item
        item_data = {
            "name": "Test Item",
            "description": "This is a test item"
        }
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/items/{item_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == item_data["name"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_update_item(self):
        """Test updating an item."""
        # First create an item
        item_data = {
            "name": "Test Item",
            "description": "Original description"
        }
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "description": "Updated description"
        }
        response = client.put(f"/api/items/{item_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["description"] == update_data["description"]
    
    @pytest.mark.skip(reason="Requires AstraDB connection")
    def test_delete_item(self):
        """Test deleting an item."""
        # First create an item
        item_data = {
            "name": "Test Item",
            "description": "To be deleted"
        }
        create_response = client.post("/api/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/items/{item_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/items/{item_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_item(self):
        """Test retrieving a non-existent item returns 404."""
        response = client.get("/api/items/nonexistent-id")
        assert response.status_code == 404

# Made with Bob
