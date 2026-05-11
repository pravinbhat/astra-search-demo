# Astra RAG Demo

A simple FastAPI application with AstraDB Data API integration for movie CRUD operations. This project serves as a foundation for building RAG (Retrieval-Augmented Generation) applications with search capabilities.

## Features

- ✅ FastAPI framework with Python 3.14.4
- ✅ AstraDB Data API integration
- ✅ RESTful CRUD operations
- ✅ Pydantic data validation
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ Health check endpoint
- ✅ Comprehensive test suite
- ✅ Environment-based configuration

## Project Structure

```
astra-rag-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic schemas
│   ├── database.py          # AstraDB client wrapper
│   └── routers/
│       ├── __init__.py
│       ├── health.py        # Health check endpoint
│       └── movies.py        # Movie CRUD endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── .env.example             # Example environment variables
├── .gitignore
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
├── LICENSE
└── README.md
```

## Prerequisites

- Python 3.13 (Python 3.14 is not yet fully supported by all dependencies)
- AstraDB account and database
- AstraDB Application Token

## Setup

### Quick Setup (Recommended)

Use the automated setup script:

```bash
# Make the script executable (if not already)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:
- Check your Python version compatibility
- Remove old virtual environment if it exists
- Create a new virtual environment with the correct Python version
- Install all dependencies
- Create .env file from template

### Manual Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/pravinbhat/astra-rag-demo.git
cd astra-rag-demo
```

#### 2. Check Python Version

**IMPORTANT**: You must use Python 3.13. Python 3.14 is NOT supported.

```bash
# Check your Python version
python3 --version

# If you have Python 3.14, install a compatible version:
# On macOS with Homebrew:
brew install python@3.13

# On Ubuntu/Debian:
sudo apt install python3.13

# On other systems, download from python.org
```

#### 3. Create Virtual Environment with Correct Python Version

```bash
# If you have multiple Python versions, specify the correct one:
python3.13 -m venv venv

# Or if python3 points to a compatible version (3.11-3.13):
python3 -m venv venv

# Activate the virtual environment:
# On macOS/Linux (bash/zsh)
source venv/bin/activate

# On macOS/Linux (fish shell)
source venv/bin/activate.fish

# On Windows
venv\Scripts\activate

# Verify the Python version in the venv:
python --version  # Should show 3.13.x
```

#### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Configure Environment Variables

Copy the example environment file and update with your AstraDB credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your AstraDB credentials:

```env
ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_KEYSPACE=default_keyspace
COLLECTION_NAME=movie_reviews
```

#### Getting AstraDB Credentials

1. Go to [AstraDB Console](https://astra.datastax.com/)
2. Create a new database or use an existing one
3. Get your API Endpoint from the database dashboard
4. Generate an Application Token with appropriate permissions
5. Note your keyspace name (default is usually `default_keyspace`)

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check

```bash
GET /health
```

Returns application health status and AstraDB connection status.

### Root

```bash
GET /
```

Returns basic application information.

### Movie Reviews CRUD Operations

The API maps to documents in the `movie_reviews` AstraDB collection.

#### Create Movie Review

```bash
POST /api/movies
Content-Type: application/json

{
  "title": "Inception",
  "reviewid": "review-123",
  "creationdate": "2024-01-01T12:00:00Z",
  "criticname": "Jane Critic",
  "originalscore": "4/5",
  "reviewstate": "published",
  "$vectorize": "A smart, visually striking sci-fi thriller with emotional depth."
}
```

#### List Movie Reviews

```bash
GET /api/movies?skip=0&limit=100
```

Query parameters:
- `skip`: Number of movie review documents to skip (default: 0)
- `limit`: Maximum number of movie review documents to return (default: 100, max: 1000)

#### Get Movie Review by ID

```bash
GET /api/movies/{movie_id}
```

#### Update Movie Review

```bash
PUT /api/movies/{movie_id}
Content-Type: application/json

{
  "reviewstate": "approved",
  "$vectorize": "Updated review text for the embedding source."
}
```

#### Delete Movie Review

```bash
DELETE /api/movies/{movie_id}
```

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

Run specific test file:

```bash
pytest tests/test_api.py
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API documentation
  - Try out API endpoints directly from the browser
  
- **ReDoc**: http://localhost:8000/redoc
  - Alternative API documentation with a different UI

## Example Usage

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Create a movie review
curl -X POST http://localhost:8000/api/movies \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Movie",
    "reviewid": "review-001",
    "creationdate": "2024-01-01T12:00:00Z",
    "criticname": "Alex Reviewer",
    "originalscore": "3.5/5",
    "reviewstate": "published",
    "$vectorize": "A compelling drama with strong performances."
  }'

# List all movie reviews
curl http://localhost:8000/api/movies

# Get specific movie review (replace {movie_id} with actual ID)
curl http://localhost:8000/api/movies/{movie_id}

# Update movie review
curl -X PUT http://localhost:8000/api/movies/{movie_id} \
  -H "Content-Type: application/json" \
  -d '{"reviewstate": "approved"}'

# Delete movie review
curl -X DELETE http://localhost:8000/api/movies/{movie_id}
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a movie review
response = requests.post(
    f"{BASE_URL}/api/movies",
    json={
        "title": "Python Movie",
        "reviewid": "review-python-001",
        "creationdate": "2024-01-01T12:00:00Z",
        "criticname": "Python Critic",
        "originalscore": "8/10",
        "reviewstate": "draft",
        "$vectorize": "Created from Python using the movie reviews API."
    }
)
movie = response.json()
print(f"Created movie review: {movie['id']}")

# Get the movie review
response = requests.get(f"{BASE_URL}/api/movies/{movie['id']}")
print(response.json())

# Update the movie review
response = requests.put(
    f"{BASE_URL}/api/movies/{movie['id']}",
    json={"reviewstate": "published"}
)
print(response.json())

# Delete the movie review
response = requests.delete(f"{BASE_URL}/api/movies/{movie['id']}")
print(f"Deleted: {response.status_code == 204}")
```

## Development

### Code Style

This project follows PEP 8 style guidelines. Format your code before committing:

```bash
# Install development dependencies
pip install black ruff

# Format code
black app/ tests/

# Lint code
ruff check app/ tests/
```

### Adding New Endpoints

1. Create a new router file in `app/routers/`
2. Define your endpoints using FastAPI decorators
3. Include the router in `app/main.py`

Example:

```python
# app/routers/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/my-feature", tags=["My Feature"])

@router.get("/")
async def list_items():
    return {"items": []}
```

```python
# app/main.py
from app.routers import my_feature

app.include_router(my_feature.router)
```

## Future Enhancements

This is a basic CRUD application. Future enhancements will include:

- 🔄 Document ingestion and processing
- 🤖 Embedding generation for vector search
- 🔍 Vector search capabilities
- 🔀 Hybrid search (vector + keyword)
- 📊 RAG pipeline implementation
- 🧠 LLM integration for question answering
- 📈 Performance monitoring and metrics

## Troubleshooting

### AstraDB Connection Issues

If you see "Failed to connect to AstraDB" in the logs:

1. Verify your `.env` file has correct credentials
2. Check that your AstraDB database is active
3. Ensure your Application Token has the necessary permissions
4. Verify the API endpoint URL is correct

### Import Errors

If you see import errors when running the application:

1. Make sure you've activated your virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Verify Python version: `python --version` (should be 3.14.4 or higher)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [AstraDB Documentation](https://docs.datastax.com/en/astra/home/astra.html)
- [AstraDB Python Client](https://docs.datastax.com/en/astra-serverless/docs/develop/dev-with-python.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [AstraDB Community](https://community.datastax.com/)
- Review the [FastAPI discussions](https://github.com/tiangolo/fastapi/discussions)