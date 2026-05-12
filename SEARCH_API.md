# Search API Documentation

## Overview

The search endpoint allows you to query library books using flexible filter predicates powered by AstraDB's Data API via the astrapy package.

## Endpoint

**POST** `/api/library-books/search`

## Request Body

```json
{
  "filter": {
    // Filter predicates (see examples below)
  },
  "skip": 0,
  "limit": 100
}
```

### Parameters

- **filter** (required): Dictionary containing filter predicates for searching documents
- **skip** (optional): Number of documents to skip for pagination (default: 0, min: 0)
- **limit** (optional): Maximum number of documents to return (default: 100, min: 1, max: 1000)

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
      "due_date": null
    }
  ],
  "total": 1
}
```

## Example Requests

### 1. Search by Author

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"author": "John Anthony"},
    "skip": 0,
    "limit": 10
  }'
```

### 2. Search by Rating Range

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"rating": {"$gte": 4.0}},
    "skip": 0,
    "limit": 20
  }'
```

### 3. Search Available Books by Genre

```bash
curl -X POST "http://localhost:8000/api/library-books/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "genres": {"$in": ["Science Fiction", "Fantasy"]},
      "is_checked_out": false
    },
    "skip": 0,
    "limit": 50
  }'
```

### 4. Search by Publication Year Range

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

### 5. Complex Multi-Criteria Search

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
    "skip": 0,
    "limit": 25
  }'
```

## Python Example

```python
import requests

# Search for available science fiction books with high ratings
response = requests.post(
    "http://localhost:8000/api/library-books/search",
    json={
        "filter": {
            "genres": {"$in": ["Science Fiction"]},
            "rating": {"$gte": 4.0},
            "is_checked_out": False
        },
        "skip": 0,
        "limit": 10
    }
)

data = response.json()
print(f"Found {data['total']} books")
for book in data['library_books']:
    print(f"- {book['title']} by {book['author']} (Rating: {book['rating']})")
```

## Error Responses

### 500 Internal Server Error
```json
{
  "detail": "Search failed: <error message>"
}
```

## Notes

- The search uses AstraDB's native filter capabilities via the astrapy package
- All filter operations are performed server-side for optimal performance
- Pagination is supported through `skip` and `limit` parameters
- The `total` field in the response indicates the total number of matching documents (not just the returned page)
- Empty filter `{}` will return all documents (subject to pagination limits)

## Implementation Details

The search endpoint is implemented using:
- **FastAPI** for the REST API framework
- **astrapy** for AstraDB Data API integration
- **Pydantic** for request/response validation

The search flow:
1. Request validation using `SearchFilter` Pydantic model
2. Filter predicates passed to `db_client.search_library_books()`
3. AstraDB collection's `find()` method executes the query
4. Results are normalized and returned with total count