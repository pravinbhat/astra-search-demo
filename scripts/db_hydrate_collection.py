import json
from pathlib import Path
from db_connect import connect_to_database, settings
from astrapy.data_types import DataAPIDate


def main() -> None:
    database = connect_to_database()

    collection = database.get_collection(settings.collection_name)

    # Get the path relative to the script's location
    script_dir = Path(__file__).parent
    data_file_path = script_dir.parent / "data" / "quickstart_dataset.json"

    # Read the JSON file and parse it into a JSON array
    with open(data_file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)

    # Assemble the documents to insert:
    # - Convert the date string into a DataAPIDate
    # - Add a $vectorize field
    documents = [
        {
            **data,
            "due_date": (
                DataAPIDate.from_string(data["due_date"])
                if data.get("due_date")
                else None
            ),
            "$vectorize": (
                f"summary: {data['summary']} | genres: {', '.join(data['genres'])}"
            ),
        }
        for data in json_data
    ]

    # Insert the data
    inserted = collection.insert_many(documents)

    print(f"Inserted {len(inserted.inserted_ids)} documents.")


if __name__ == "__main__":
    main()