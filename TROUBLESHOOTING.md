# Troubleshooting

## Quick Diagnostics

If you're experiencing issues, check these first:

1. Verify `.env` file exists and contains all required variables
2. Ensure Python 3.13 is being used: `python --version`
3. Check AstraDB console to confirm database is active
4. Verify collection setup by running: `python -m scripts.db_create_collection`

## Collection not found

**Symptom:** API returns errors about missing collection

**Solution:** Make sure your `.env` contains:

```env
COLLECTION_NAME=library_books
```

Then create the collection:
```bash
python -m scripts.db_create_collection
```

## AstraDB connection issues

**Symptom:** Startup logs show connection failures or timeout errors

**Solutions:**

- Verify the endpoint URL format: `https://[database-id]-[region].apps.astra.datastax.com`
- Verify the application token starts with `AstraCS:`
- Verify the keyspace name matches your database
- Check that your database is in "Active" state in AstraDB console
- Ensure your IP is not blocked (check AstraDB security settings)

## Token expiration or permission errors

**Symptom:** `401 Unauthorized` or permission denied errors

**Solutions:**

- Generate a new application token from AstraDB console
- Ensure token has "Database Administrator" role
- Update `ASTRA_DB_APPLICATION_TOKEN` in `.env`
- Restart the application

## Vectorize/Embedding generation errors

**Symptom:** Errors during collection creation or data insertion related to embeddings

**Solutions:**

- Verify `EMBEDDING_PROVIDER` and `EMBEDDING_MODEL_NAME` in `.env`
- Ensure the embedding model is available in your AstraDB region
- Check AstraDB documentation for supported embedding providers
- Default configuration uses: `nvidia/nv-embedqa-e5-v5`

## Data hydration failures

**Symptom:** Script fails when loading sample data

**Solutions:**

- Ensure collection exists before running hydration script
- Check that `data/quickstart_dataset.json` exists and is valid JSON
- Verify sufficient database capacity/limits
- Re-run `python -m scripts.db_create_collection` before hydrating if collection setup is uncertain

## Python version issues

**Symptom:** Import errors or compatibility issues

**Solution:** Use Python 3.13 for local setup:

```bash
python3.13 --version
python3.13 -m venv venv
source venv/bin/activate
```
