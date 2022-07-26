import logging
from typing import TypeVar, List

import mysql.connector as mysql

from settings.settings import Settings

FILTERS = ["year", "city"]


class SimpleORM:
    """A base ORM to connect to Database and send queries"""

    T = TypeVar("T")  # Declare type variable for generic use

    def __init__(self) -> None:
        """Create the connection to the database

        If the connection fails, raise an error to exit the execution of the program.
        """
        settings = Settings()
        try:
            db = mysql.connect(
                host=settings.database_host,
                database=settings.database_name,
                user=settings.database_user,
                password=settings.database_password,
                port=settings.database_port,
            )
            self.db = db
            self.cursor = db.cursor()
        except mysql.Error as e:
            logging.error(f"Error connecting to database: \n{e}")
            raise

    def __del__(self):
        """Maintains the cursor alive until the object is clean"""
        self.cursor.close()

    def __do_query(self, **kwargs) -> List[dict]:
        """Create a query to database

        Example of arguments
        - table: name where the query is executed
        - fields: a list of fields name
        - params: a list of filters to be applied

        This methods means to be private
        """
        fields = ", ".join(kwargs["fields"])
        params = kwargs["params"]

        filters = ""

        for key, value in params.items():
            # Only validate filters that are supposed to be in the query
            if key in FILTERS:
                filters = filters + f"{key}='{value[0]}' AND "

        # remove last AND and add the were
        if filters:
            filters = filters[:-4]
            filters = f"AND {filters}"

        # I going to hack the query to filter as in the challenger,
        # fdor the limitations of this SimpleORM class and for the sake of
        # simplicity in the challenger
        query = f"""SELECT {fields} FROM {kwargs['table']}
        INNER JOIN status_history sh on property.id = sh.property_id
        INNER JOIN status s on sh.status_id = s.id
        WHERE s.name IN ('pre_venta', 'vendido', 'en_venta')
        AND sh.update_date IN (SELECT MAX(sh.update_date) FROM status_history)
        {filters}
        GROUP BY sh.property_id
        """

        logging.info(query)

        objects = []
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for row in results:
            #  We zip fields and row to create a dictionary
            result = zip(kwargs["fields"], row)
            objects.append(dict(result))
        return objects

    def get_objects(self, T, **query_params) -> List[T]:
        """Return a list of objects from T model."""
        table_name = T.__name__.lower()

        kwargs = {
            "table": table_name,
            "fields": list(T.__annotations__.keys()),
            "params": query_params,
        }
        results = self.__do_query(**kwargs)

        # Create a list of objects to return
        list_of_objects = []
        for o in results:
            list_of_objects.append(T(**o))

        return list_of_objects
