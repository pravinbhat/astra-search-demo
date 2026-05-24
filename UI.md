# UI User Guide

## Overview

Search through a library of books using filters, natural language queries, keywords, or a combination of methods.

## Search Methods

### Filter Search
Build custom searches using book attributes:
- Author, Title, Genres, Rating, Publication Year, Pages, Checkout Status
- Combine multiple filters to narrow results

### Semantic Search
Natural language queries that understand meaning, not just keywords.

Examples: "books about resilience and survival", "dystopian futures with strong female protagonists"

### Lexical Search
Traditional keyword-based search in indexed text fields.

This is useful for keyword-oriented terms that may not be surfaced reliably by semantic search alone. In this app, lexical search can be especially helpful for finding books by author name or ISBN when those values are indexed.

Examples: "dystopian survival", "quantum physics", "artificial intelligence"

### Hybrid Search
Combines semantic understanding and keyword matching for comprehensive results.

Use this when you want the benefits of semantic discovery together with direct matching on indexed terms such as author names and ISBN values.

![Hybrid Search Mode](app/static/UI_HybridMode.png)

### Comparison Mode
View results from all four methods side-by-side to see how different approaches find different books.

![Comparison Mode](app/static/UI_CompareMode.png)

## Quick Start

**Filter Search**: Add filters → Set criteria → Search

**Semantic/Lexical Search**: Enter query or keywords → Add optional filters → Search

**Hybrid Search**: Enter natural language query + keywords → Add optional filters → Search

A practical pattern in this app is to use the semantic query for topic intent and the keywords field for exact terms like author names or ISBNs.

**Comparison Mode**: Enter semantic query + lexical keywords → Compare results

## Result Cards

Each book shows:
- Title, Author, Star Rating, Genres
- Summary (expandable)
- Checkout Status
- Similarity Score (for semantic/hybrid searches)

Books appearing in multiple results (Comparison Mode) are highlighted.

## Troubleshooting

**Page won't load**: Refresh browser, clear cache, verify URL

**Search not working**: Check query/filters, try different terms, refresh page
