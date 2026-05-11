# Astra RAG Demo

A lightweight demo app for working with AstraDB and a `movie_reviews` collection prepared for vector and hybrid search use cases.

This project is centered around movie review documents stored in AstraDB, where:

- `$vectorize` contains the review text used for embedding generation
- AstraDB generates and stores the vector automatically
- the collection can be used later for semantic or hybrid retrieval workflows

## What this demo is for

This project focuses on the **retrieval** side of RAG.

It assumes your movie review documents and their related embeddings are already present in AstraDB / Astra Vector DB. It does **not** focus on ingestion-time concerns such as chunking, embedding generation pipelines, or document preprocessing.

Use this project to:

- connect a local app to an existing AstraDB collection
- work with movie review documents through a simple API
- explore retrieval-oriented workflows for vector and hybrid search
- validate the data access layer before adding dedicated RAG retrieval endpoints

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

## Run the app

```bash
uvicorn app.main:app --reload
```

Once running:

- API base URL: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

## API overview

The API works with the `movie_reviews` collection through the `movie_review` entity.

For the full endpoint contract, payload examples, and response shapes, see [API.md](API.md).

## What’s next

Planned enhancements for this demo include:

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
---

Built with [IBM Bob](https://bob.ibm.com/) as my pair-programming partner.