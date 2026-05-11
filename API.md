# API Reference

This document contains the API contract for working with the `movie_reviews` collection through the `movie_review` entity.

## Base URL

```text
http://localhost:8000
```

## Endpoints

```text
POST   /api/movie-reviews
GET    /api/movie-reviews
GET    /api/movie-reviews/{movie_review_id}
PUT    /api/movie-reviews/{movie_review_id}
DELETE /api/movie-reviews/{movie_review_id}
```

## Entity shape

Example payload:

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

Important notes:

- `$vectorize` can be sent on create and update
- `$vector` is not accepted from clients
- `$vector` is not returned by the API
- AstraDB manages vector generation internally
- `$vectorize` may not always be returned in read responses, depending on AstraDB document return behavior

## Create movie review

```bash
curl -X POST http://localhost:8000/api/movie-reviews \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "reviewid": "review-123",
    "creationdate": "2024-01-01T12:00:00Z",
    "criticname": "Jane Critic",
    "originalscore": "4/5",
    "reviewstate": "published",
    "$vectorize": "A smart, visually striking sci-fi thriller with emotional depth."
  }'
```

## List movie reviews

```bash
curl http://localhost:8000/api/movie-reviews
```

## Get movie review by ID

```bash
curl http://localhost:8000/api/movie-reviews/{movie_review_id}
```

## Update movie review

```bash
curl -X PUT http://localhost:8000/api/movie-reviews/{movie_review_id} \
  -H "Content-Type: application/json" \
  -d '{
    "reviewstate": "approved",
    "$vectorize": "Updated review text for the embedding source."
  }'
```

## Delete movie review

```bash
curl -X DELETE http://localhost:8000/api/movie-reviews/{movie_review_id}
```

## Response shape

Example list response:

```json
{
  "movie_reviews": [
    {
      "id": "doc-id",
      "title": "Inception",
      "reviewid": "review-123",
      "creationdate": "2024-01-01T12:00:00Z",
      "criticname": "Jane Critic",
      "originalscore": "4/5",
      "reviewstate": "published",
      "$vectorize": null,
      "embedding": null
    }
  ],
  "total": 1
}