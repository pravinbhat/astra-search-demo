# Astra RAG Demo

A lightweight demo app for working with AstraDB and a `movie_reviews` collection prepared for vector and hybrid search use cases.

This project is centered around movie review documents stored in AstraDB, where:

- `$vectorize` contains the review text used for embedding generation
- AstraDB generates and stores the vector automatically
- the collection can be used later for semantic or hybrid retrieval workflows

## What this demo is for

Use this project to:

- connect a local app to an AstraDB collection
- work with movie review documents through a simple API
- prepare a dataset for vector and hybrid search experiments
- validate document ingestion and retrieval before adding search endpoints

## AstraDB collection

This app is designed to work with a collection named:

```text
movie_reviews
```

Expected document fields include:

- `_id`
- `title`
- `reviewid`
- `creationdate`
- `criticname`
- `originalscore`
- `reviewstate`
- `$vectorize`
- `embedding`
- `$vector`

Notes:

- `$vectorize` is used as the source text for AstraDB embedding generation
- `$vector` is not exposed through the API
- the current API focuses on CRUD-style access to movie review documents
- search endpoints can be added next on top of the same collection

## Why this matters for hybrid search

AstraDB hybrid search combines:

- semantic similarity from vectors
- keyword / lexical matching from text search

That makes a movie reviews dataset like this useful for questions such as:

- "find reviews similar to this review text"
- "find reviews about sci-fi movies with strong acting"
- "find reviews mentioning Nolan with positive sentiment"
- "find reviews semantically similar to a user query, while also matching specific critic or score filters"

This demo sets up the collection and API shape needed for those next steps.

## Setup

### Quick setup

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:

- check Python compatibility
- create a virtual environment
- install dependencies
- create a local `.env` file from the template

### Manual setup

#### 1. Clone the repository

```bash
git clone https://github.com/pravinbhat/astra-rag-demo.git
cd astra-rag-demo
```

#### 2. Use Python 3.13

```bash
python3.13 --version
```

If needed, create a virtual environment:

```bash
python3.13 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure environment variables

```bash
cp .env.example .env
```

Update `.env` with your AstraDB values:

```env
ASTRA_DB_API_ENDPOINT=https://your-database-id-your-region.apps.astra.datastax.com
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_KEYSPACE=default_keyspace
COLLECTION_NAME=movie_reviews
```

### Getting AstraDB credentials

1. Open [AstraDB Console](https://astra.datastax.com/)
2. Select your database
3. Copy the API endpoint
4. Create or use an application token
5. confirm the keyspace name

## Run the app

```bash
uvicorn app.main:app --reload
```

Once running:

- API base URL: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

## API overview

The API works with the `movie_reviews` collection through the `movie_review` entity.

Available endpoints:

```text
POST   /api/movie-reviews
GET    /api/movie-reviews
GET    /api/movie-reviews/{movie_review_id}
PUT    /api/movie-reviews/{movie_review_id}
DELETE /api/movie-reviews/{movie_review_id}
```

### Example create payload

```json
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

### Important API behavior

- `$vectorize` can be sent on create/update
- `$vector` is not accepted from clients
- `$vector` is not returned by the API
- AstraDB manages vector generation internally
- `$vectorize` may not always be returned in read responses, depending on AstraDB document return behavior

## Quick usage example

### Create a movie review

```bash
curl -X POST http://localhost:8000/api/movie-reviews \
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
```

### List movie reviews

```bash
curl http://localhost:8000/api/movie-reviews
```

## What’s next

The next natural enhancement for this demo is search:

- vector search using the stored embeddings
- keyword search over review text and metadata
- hybrid search combining both approaches
- optional metadata filtering by critic, review state, score, or title

## Troubleshooting

### Collection not found

Make sure your `.env` contains:

```env
COLLECTION_NAME=movie_reviews
```

### AstraDB connection issues

If startup logs show AstraDB connection failures:

- verify the endpoint URL
- verify the application token
- verify the keyspace
- verify the collection exists in AstraDB

### Python version issues

Use Python 3.13 for local setup.

## Resources

- [AstraDB Documentation](https://docs.datastax.com/en/astra/home/astra.html)
- [AstraDB Python Client](https://docs.datastax.com/en/astra-serverless/docs/develop/dev-with-python.html)

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE).