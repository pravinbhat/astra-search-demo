from astrapy import DataAPIClient, Database
from pydantic_settings import BaseSettings, SettingsConfigDict


def connect_to_database() -> Database:
    """
    Connects to a DataStax Astra database.
    This function retrieves the database endpoint and application token from the
    environment variables `ASTRA_DB_API_ENDPOINT` and `ASTRA_DB_APPLICATION_TOKEN`.

    Returns:
        Database: An instance of the connected database.

    Raises:
        RuntimeError: If the environment variables `ASTRA_DB_API_ENDPOINT` or
        `ASTRA_DB_APPLICATION_TOKEN` are not defined.
    """

    if not settings.astra_db_application_token or not settings.astra_db_api_endpoint:
        raise RuntimeError(
            "Environment variables ASTRA_DB_API_ENDPOINT and ASTRA_DB_APPLICATION_TOKEN must be defined"
        )

    # Create an instance of the `DataAPIClient` class with the token
    client = DataAPIClient(settings.astra_db_application_token)

    # Get the database specified by your endpoint
    database = client.get_database(settings.astra_db_api_endpoint)

    print(f"Connected to database {database.info().name}")

    return database

class Settings(BaseSettings):
    """Script settings loaded from environment variables."""
    
    # AstraDB settings
    astra_db_api_endpoint: str
    astra_db_application_token: str
    astra_db_keyspace: str
    collection_name: str
    
    # Embedding settings
    embedding_provider: str
    embedding_model_name: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()