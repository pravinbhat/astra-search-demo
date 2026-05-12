# Troubleshooting

## Collection not found

Make sure your `.env` contains:

```env
COLLECTION_NAME=library_books
```

## AstraDB connection issues

If startup logs show AstraDB connection failures:

- verify the endpoint URL
- verify the application token
- verify the keyspace
- verify the collection exists in AstraDB

## Python version issues

Use Python 3.13 for local setup.