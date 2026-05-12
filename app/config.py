"""
Configuration management using Pydantic Settings.
Loads configuration from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = "Astra RAG Demo"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # AstraDB settings
    astra_db_api_endpoint: str
    astra_db_application_token: str
    astra_db_keyspace: str = "default_keyspace"
    collection_name: str = "library_books"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()

# Made with Bob
