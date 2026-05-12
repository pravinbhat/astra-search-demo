from scripts.script_utils import (
    build_vectorized_documents,
    get_collection,
    get_data_file_path,
    load_json_file,
)


def main() -> None:
    collection = get_collection()

    deleted = collection.delete_many({})
    print(f"Truncated collection by deleting {deleted.deleted_count} documents.")

    json_data = load_json_file(get_data_file_path())
    documents = build_vectorized_documents(json_data)
    inserted = collection.insert_many(documents)
    print(f"Inserted {len(inserted.inserted_ids)} documents.")


if __name__ == "__main__":
    main()