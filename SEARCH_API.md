# Search API Documentation

## Overview

The search endpoint allows you to query library books using filter predicates, semantic queries, or both, powered by AstraDB's Data API via the astrapy package.

## Endpoint

**POST** `/api/library-books/search`

## Request Body

```json
{
  "filter": {
    // Optional filter predicates (see examples below)
  },
  "query": "Optional semantic search query",
  "skip": 0,
  "limit": 100
}
```

### Parameters

- **filter** (optional): Dictionary containing filter predicates for searching documents
- **query** (optional): Semantic search query/prompt used for AstraDB vector search
- **skip** (optional): Number of documents to skip for pagination (default: 0, min: 0)
- **limit** (optional): Maximum number of documents to return (default: 100, min: 1, max: 1000)

## Search Modes

### 1. Filter Search
Use only the `filter` field to perform predicate-based search.

### 2. Semantic Search
Use only the `query` field to perform semantic vector search.

### 3. Semantic Filter Search
Use both `filter` and `query` to constrain semantic search results using metadata predicates.

## Filter Operators

### Equality
Match documents where a field equals a specific value.

```json
{
  "filter": {
    "author": "John Anthony"
  }
}
```

### Comparison Operators
- `$eq`: Equal to
- `$ne`: Not equal to
- `$gt`: Greater than
- `$gte`: Greater than or equal to
- `$lt`: Less than
- `$lte`: Less than or equal to

```json
{
  "filter": {
    "rating": {"$gte": 4.0},
    "number_of_pages": {"$lt": 500}
  }
}
```

### Array Operators
- `$in`: Match any value in array
- `$nin`: Match none of the values in array

```json
{
  "filter": {
    "genres": {"$in": ["Science Fiction", "Fantasy"]}
  }
}
```

### Multiple Conditions
Combine multiple filter conditions (implicit AND).

```json
{
  "filter": {
    "author": "John Anthony",
    "is_checked_out": false,
    "rating": {"$gte": 4.0}
  }
}
```

## Response

```json
{
  "library_books": [
    {
      "id": "doc-id-123",
      "title": "Book Title",
      "author": "Author Name",
      "number_of_pages": 350,
      "rating": 4.5,
      "publication_year": 2020,
      "summary": "Book summary...",
      "genres": ["Fiction", "Drama"],
      "metadata": {
        "isbn": "978-1-234567-89-0",
        "language": "English",
        "edition": "First Edition"
      },
      "is_checked_out": false,
      "borrower": null,
      "due_date": null,
      "$similarity": 0.91
    }
  ],
  "total": 1
}
```

## Example Requests

### 1. Filter Search by Author

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"author": "John Anthony"},
    "skip": 0,
    "limit": 10
  }'
```

### 2. Semantic Search by Query

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "books about resilience and survival",
    "skip": 0,
    "limit": 10
  }'
```

### 3. Semantic Filter Search by Genre

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "genres": {"$in": ["Science Fiction", "Fantasy"]},
      "is_checked_out": false
    },
    "query": "books about space exploration and adventure",
    "skip": 0,
    "limit": 50
  }'
```

### 4. Filter Search by Publication Year Range

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "publication_year": {"$gte": 2000, "$lte": 2020}
    },
    "skip": 0,
    "limit": 100
  }'
```

### 5. Semantic Filter Search with Multiple Criteria

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "author": "John Anthony",
      "rating": {"$gte": 3.5},
      "number_of_pages": {"$lt": 500},
      "is_checked_out": false
    },
    "query": "books about ambition and social class",
    "skip": 0,
    "limit": 25
  }'
```

## Python Example

```python
import requests

# Semantic filter search for available science fiction books
response = requests.post(
    "http://localhost:8000/api/library-books/search",
    json={
        "filter": {
            "genres": {"$in": ["Science Fiction"]},
            "rating": {"$gte": 4.0},
            "is_checked_out": False
        },
        "query": "books about futuristic worlds and survival",
        "skip": 0,
        "limit": 10
    }
)

data = response.json()
print(f"Found {data['total']} books")
for book in data['library_books']:
    print(
        f"- {book['title']} by {book['author']} "
        f"(Rating: {book['rating']}, Similarity: {book.get('$similarity')})"
    )
```

## Error Responses

### 500 Internal Server Error
```json
{
  "detail": "Search failed: <error message>"
}
```

## Notes

- The search uses AstraDB's native filter capabilities and vector search support via the astrapy package
- All filter operations are performed server-side for optimal performance
- Semantic search uses the collection's `$vectorize` configuration
- Pagination is supported through `skip` and `limit` parameters
- The `total` field in the response indicates the number of results iterated for the current search mode
- Empty filter `{}` with no query will return all documents (subject to pagination limits)
- Semantic results may include AstraDB's `$similarity` field

## Implementation Details

The search endpoint is implemented using:
- **FastAPI** for the REST API framework
- **astrapy** for AstraDB Data API integration
- **Pydantic** for request/response validation

The search flow:
1. Request validation using `LibraryBookSearchRequest` Pydantic model
2. Filter-only requests call `db_client.search_library_books()`
3. Requests with `query` call `db_client.semantic_search_library_books()`
4. AstraDB collection's `find()` method executes the query with optional vector sorting
5. Results are normalized and returned with total count