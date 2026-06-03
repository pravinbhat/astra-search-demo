import json
from pathlib import Path
from typing import Any

from astrapy.constants import VectorMetric
from astrapy.data_types import DataAPIDate
from astrapy.info import CollectionDefinition, CollectionVectorOptions, VectorServiceOptions

from app.config import settings
from app.database import get_connected_database


def get_database():
    """Return a connected AstraDB database handle."""
    return get_connected_database()


def get_collection(name: str | None = None):
    """Return a collection handle using the configured default if not provided."""
    database = get_database()
    return database.get_collection(name or settings.collection_name)


def build_collection_definition() -> CollectionDefinition:
    """Build the vector-enabled collection definition with DOT_PRODUCT metric and lexical search."""
    return (
        CollectionDefinition.builder()
        .set_vector_service(settings.embedding_provider, settings.embedding_model_name)
        .set_vector_metric(VectorMetric.DOT_PRODUCT)
        .set_lexical({
            "tokenizer": {"name": "standard", "args": {}},
            "filters": [
                {"name": "lowercase"},
                {"name": "stop"},
                {"name": "porterstem"},
                {"name": "asciifolding"},
            ],
        })
        .build()
    )


def get_data_file_path(filename: str = "quickstart_dataset.json") -> Path:
    """Return a path under the repository data directory."""
    return Path(__file__).resolve().parent.parent / "data" / filename


def load_json_file(path: Path) -> list[dict[str, Any]]:
    """Load a JSON array from disk."""
    with open(path, "r", encoding="utf8") as file:
        return json.load(file)


def build_vectorized_documents(json_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert raw seed data into Astra-ready documents."""
    return [
        {
            **data,
            "due_date": (
                DataAPIDate.from_string(data["due_date"]) if data.get("due_date") else None
            ),
            "$hybrid": (
                f"title: {data['title']} | author: {data['author']} | summary: {data['summary']} | genres: {', '.join(data['genres'])} | isbn: {data.get('metadata', {}).get('isbn', 'N/A')}"
            ),
        }
        for data in json_data
    ]


# Made with Bob
