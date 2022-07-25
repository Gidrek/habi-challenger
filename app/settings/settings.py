import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Class that have settings to be used in the application"""

    hostname: str = os.environ.get("HOSTNAME", "localhost")
    port: int = os.environ.get("PORT", 8000)
    database_host: str = os.environ.get("DATABASE_HOST", "localhost")
    database_name: str = os.environ.get("DATABASE_NAME", "db_habi")
    database_user: str = os.environ.get("DATABASE_USER", "dbuser")
    database_password: str = os.environ.get("DATABASE_PASSWORD", "dbpassword")
    database_port: str = os.environ.get("DATABASE_PORT", 3306)
