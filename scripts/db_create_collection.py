from app.config import settings
from scripts.db_connect import connect_to_database
from scripts.script_utils import build_collection_definition


def main() -> None:
    database = connect_to_database()
    collection = database.create_collection(
        name=settings.collection_name,
        definition=build_collection_definition(),
    )
    print(f"Created collection {collection.full_name}")


if __name__ == "__main__":
    main()
