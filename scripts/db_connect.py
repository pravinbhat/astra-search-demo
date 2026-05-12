from astrapy import Database

from app.config import settings
from app.database import get_connected_database


def connect_to_database() -> Database:
    """Return a connected AstraDB database handle using shared app config."""
    database = get_connected_database()
    print(f"Connected to database {database.info().name}")
    return database