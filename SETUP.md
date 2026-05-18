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

# Embedding configuration (shared by app and ingestion scripts)
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

Run the collection creation script as a module to set up the `library_books` collection with vectorize enabled:

```bash
python -m scripts.db_create_collection
```

This script:
- Reuses shared app configuration and AstraDB connection helpers
- Creates a collection with COSINE vector metric
- Configures AstraDB's vectorize feature with the embedding provider and model specified in your `.env` file

### 2. Hydrate the collection

Load the sample library books dataset into the collection by running the hydration script as a module:

```bash
python -m scripts.db_hydrate_collection
```

This script:
- Reuses shared helpers for collection access, file loading, and document preparation
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

**Access:**
- Web UI: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

See [UI.md](UI.md) for UI usage or [API.md](API.md) for REST API.

## Testing

Run tests with pytest:

```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_api.py  # Run specific test file
```

The test suite covers health checks, CRUD operations, and error handling.

## Additional Resources

- Interactive API documentation: `http://localhost:8000/docs`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions