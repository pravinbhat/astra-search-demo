# Setup

## Prerequisites

- Python 3.13 or higher
- An AstraDB account with a database created
- Application token with appropriate permissions

## Quick setup

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:

- check Python compatibility
- create a virtual environment
- install dependencies
- create a local `.env` file from the template

## Manual setup

### 1. Clone the repository

```bash
git clone https://github.com/pravinbhat/astra-search-demo.git
cd astra-search-demo
```

### 2. Use Python 3.13

```bash
python3.13 --version
```

If needed, create a virtual environment:

```bash
python3.13 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your AstraDB values:

```env
ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_KEYSPACE=default_keyspace
COLLECTION_NAME=library_books

# Embedding Configuration (for vectorize feature)
EMBEDDING_PROVIDER=nvidia
EMBEDDING_MODEL_NAME=nvidia/nv-embedqa-e5-v5
```

## Getting AstraDB credentials

1. Open [AstraDB Console](https://astra.datastax.com/)
2. Select your database
3. Copy the API endpoint
4. Create or use an application token

## Data Ingestion

The project includes scripts to create and hydrate the `library_books` collection with sample data.

### 1. Create the collection

Run the collection creation script to set up the `library_books` collection with vectorize enabled:

```bash
python scripts/db_create_collection.py
```

This script:
- Creates a collection with COSINE vector metric
- Configures AstraDB's vectorize feature with NVIDIA embeddings
- Uses the embedding provider and model specified in your `.env` file

### 2. Hydrate the collection

Load the sample library books dataset into the collection:

```bash
python scripts/db_hydrate_collection.py
```

This script:
- Reads book data from `data/quickstart_dataset.json`
- Transforms the data and adds `$vectorize` fields (summary + genres)
- Inserts documents into the collection
- AstraDB automatically generates embeddings via the vectorize feature

The sample dataset includes library books with:
- Title, author, publication year
- Summary, genres, ratings
- Checkout status and borrower information
- Metadata (ISBN, language, edition)

## Run the app

```bash
uvicorn app.main:app --reload
```

Once running:

- API base URL: `http://localhost:8000`

## Testing

The project includes comprehensive API tests using pytest.

### Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run specific test classes:

```bash
pytest tests/test_api.py::TestHealthEndpoint
pytest tests/test_api.py::TestLibraryBooksEndpoint
```

Run a specific test:

```bash
pytest tests/test_api.py::TestHealthEndpoint::test_health_check
```

### Test Coverage

The test suite includes:

- **Health Check Tests** - Verify API health endpoint and database connectivity
- **Root Endpoint Tests** - Validate welcome message and API metadata
- **CRUD Operations Tests** - Test create, read, update, and delete operations for library books
- **Error Handling Tests** - Verify 404 responses for non-existent resources

### Test Configuration

Test configuration is managed in `pytest.ini`:
- Async test support enabled
- Verbose output by default
- Short traceback format for readability

### Test Fixtures

The test suite uses fixtures defined in `tests/conftest.py` for:
- Automatic cleanup of test data
- Isolated test execution
- Database state management

## Additional Resources

- Interactive API documentation: `http://localhost:8000/docs`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions