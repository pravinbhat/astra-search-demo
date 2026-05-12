from db_connect import connect_to_database, settings
from astrapy.constants import VectorMetric
from astrapy.info import CollectionDefinition, CollectionVectorOptions, VectorServiceOptions


def main() -> None:
    database = connect_to_database()

    # Create collection definition with vectorize service
    collection_definition = CollectionDefinition(
        vector=CollectionVectorOptions(
            metric=VectorMetric.COSINE,
            service=VectorServiceOptions(
                provider=settings.embedding_provider,
                model_name=settings.embedding_model_name,
            ),
        ),
    )

    collection = database.create_collection(
        name=settings.collection_name,
        definition=collection_definition,
    )

    print(f"Created collection {collection.full_name}")


if __name__ == "__main__":
    main()
