import logging

from mysql.connector import connect, Error

from settings.settings import Settings


class SimpleORM:
    """A base ORM to connect to Database and send queries"""

    def __init__(self) -> None:
        """Create the connection to the database

        If the connection fails, raise an error to exit the execution of the program.
        """
        settings = Settings()
        try:
            with connect(
                host=settings.database_host,
                user=settings.database_user,
                password=settings.database_password,
            ) as connection:
                self.connection = connection
        except Error as e:

            logging.error(f"Error connecting to database: \n{e}")
            print(f"Error connecting to database: \n{e}")
            raise

        def do_query(self, **kwargs):
            """Create a query to database"""
