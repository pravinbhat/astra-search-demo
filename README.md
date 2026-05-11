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

## Documentation

- [SETUP.md](SETUP.md) — installation, configuration, and local run instructions
- [API.md](API.md) — endpoint contract, payloads, and response examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — common issues and fixes

## What’s next

Planned enhancements for this demo include:

- vector search using the stored embeddings
- keyword search over review text and metadata
- hybrid search combining both approaches
- optional metadata filtering by critic, review state, score, or title

## Resources

- [AstraDB Documentation](https://docs.datastax.com/en/astra/home/astra.html)
- [AstraDB Python Client](https://docs.datastax.com/en/astra-serverless/docs/develop/dev-with-python.html)

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE).
---

Built with [IBM Bob](https://bob.ibm.com/) as my pair-programming partner.