# API Reference

This document contains the API contract for working with the `library_books` collection through the `library_book` entity.

## Base URL

```text
http://localhost:8000
```

## Endpoints

```text
POST   /api/library-books
GET    /api/library-books
GET    /api/library-books/{library_book_id}
PUT    /api/library-books/{library_book_id}
DELETE /api/library-books/{library_book_id}
POST   /api/library-books/search
```

> **Note:** For detailed documentation on the search endpoint including filter search, semantic search, semantic filter search, operators, and examples, see [SEARCH_API.md](SEARCH_API.md).

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

Example single book response:

```json
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
  "$vectorize": null,
  "$similarity": 0.91,
  "embedding": null
}
```

Example list response:

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
      "$vectorize": null,
      "$similarity": 0.91,
      "embedding": null
    }
  ],
  "total": 1
}
```

## Field descriptions

- `title`: Book title (required)
- `author`: Book author (required)
- `number_of_pages`: Number of pages in the book (required, positive integer)
- `rating`: Book rating from 0 to 5 (required)
- `publication_year`: Year the book was published (required, 1000-9999)
- `summary`: Book summary or description (required)
- `genres`: Array of genre strings (required)
- `metadata`: Object containing ISBN, language, and edition (required)
- `is_checked_out`: Whether the book is currently checked out (required, boolean)
- `borrower`: Name of the person who borrowed the book (optional, null if not checked out)
- `due_date`: Due date for return if checked out (optional, ISO 8601 format string)
- `$vectorize`: Text used for embedding generation (optional, typically summary + genres)
- `$similarity`: Similarity score returned by AstraDB for semantic search results (optional)
- `embedding`: Vector embedding (read-only, managed by AstraDB)