# API Reference

REST API endpoints for the `library_books` collection.

**Base URL:** `http://localhost:8000`

**Interactive API Documentation:** `http://localhost:8000/docs`

## Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| GET | `/health` | Health check endpoint | 200 |
| POST | `/api/library-books` | Create a new library book | 201, 500 |
| GET | `/api/library-books` | List library books with pagination | 200 |
| GET | `/api/library-books/{id}` | Get a specific library book | 200, 404 |
| PUT | `/api/library-books/{id}` | Update a library book | 200, 404 |
| DELETE | `/api/library-books/{id}` | Delete a library book | 204, 404 |
| POST | `/api/library-books/search` | Search library books | 200, 500 |

> **Note:** For detailed documentation on the search endpoint including semantic search, lexical search, hybrid search, operators, and examples, see [SEARCH_API.md](SEARCH_API.md).

## Entity shape

Example payload:

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "number_of_pages": 180,
  "rating": 4.5,
  "publication_year": 1925,
  "summary": "A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream.",
  "genres": ["Fiction", "Classic", "Literary Fiction"],
  "metadata": {
    "isbn": "978-0-7432-7356-5",
    "language": "English",
    "edition": "First Edition"
  },
  "is_checked_out": false,
  "borrower": null,
  "due_date": null,
  "$vectorize": "summary: A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream. | genres: Fiction, Classic, Literary Fiction"
}
```

Important notes:

- `$vectorize` can be sent on create and update
- `$vector` is not accepted from clients
- `$vector` is not returned by the API
- AstraDB manages vector generation internally
- `$vectorize` may not always be returned in read responses, depending on AstraDB document return behavior
- `$vectorize` is typically constructed from the book's summary and genres

## Create library book

```bash
curl -X POST http://localhost:8000/api/library-books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "number_of_pages": 180,
    "rating": 4.5,
    "publication_year": 1925,
    "summary": "A classic American novel set in the Jazz Age.",
    "genres": ["Fiction", "Classic"],
    "metadata": {
      "isbn": "978-0-7432-7356-5",
      "language": "English",
      "edition": "First Edition"
    },
    "is_checked_out": false,
    "borrower": null,
    "due_date": null,
    "$vectorize": "summary: A classic American novel set in the Jazz Age. | genres: Fiction, Classic"
  }'
```

## List library books

```bash
curl http://localhost:8000/api/library-books
```

With pagination:

```bash
curl "http://localhost:8000/api/library-books?skip=0&limit=10"
```

## Get library book by ID

```bash
curl http://localhost:8000/api/library-books/{library_book_id}
```

## Update library book

```bash
curl -X PUT http://localhost:8000/api/library-books/{library_book_id} \
  -H "Content-Type: application/json" \
  -d '{
    "is_checked_out": true,
    "borrower": "John Doe",
    "due_date": "2024-12-31T23:59:59Z"
  }'
```

## Delete library book

```bash
curl -X DELETE http://localhost:8000/api/library-books/{library_book_id}
```

## Response shape

List response with pagination:

```json
{
  "library_books": [
    {
      "id": "doc-id-123",
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "number_of_pages": 180,
      "rating": 4.5,
      "publication_year": 1925,
      "summary": "A classic American novel set in the Jazz Age.",
      "genres": ["Fiction", "Classic"],
      "metadata": {
        "isbn": "978-0-7432-7356-5",
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

Single book responses return the same structure without the `library_books` array wrapper.