import logging
from typing import TypeVar, List

import mysql.connector as mysql

from settings.settings import Settings


class SimpleORM:
    """A base ORM to connect to Database and send queries"""

    T = TypeVar("T")  #  Declare type variable for generic use

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
            )
            self.db = db
            self.cursor = db.cursor()
        except mysql.Error as e:
            logging.error(f"Error connecting to database: \n{e}")
            raise

    def __del__(self):
        """Maintains the cursor alive until the object is clean"""
        self.cursor.close()

    def do_query(self, **kwargs) -> List[dict]:
        """Create a query to database

        Example of arguments
        - table: name where the query is executed
        - fields: a list of fields name
        - params: a list of filters to be applied
        """
        fields = ", ".join(kwargs["fields"])
        params = kwargs["params"]

        where_clause = "WHERE status in ('pre_venta', 'vendido', 'en_venta')"
        filters = ""

        for key, value in params.items():
            filters = filters + f"{key}='{value[0]}' AND "

        # remove last AND and add the were
        if filters:
            filters = filters[:-4]
            where_clause = f"{where_clause} AND {filters}"

        # I going to hack the query to filter as in the challenger, for time consuming
        query = f"""SELECT {fields} from {kwargs['table']}
        {where_clause}
        """

        print(query)

        objects = []
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for row in results:
            #  We zip fields and row to create a dictionary
            result = zip(kwargs["fields"], row)
            objects.append(dict(result))
        return objects

    def get_objects(self, T, **query_params) -> List[T]:
        """"""
        table_name = ""

        #  Transforms the class to a mysql database
        if T.__name__.lower()[-1] == "y":
            table_name = f"{T.__name__.lower()[:-1]}ies"
        else:
            table_name = f"{T.__name__.lower()}s"

        kwargs = {
            "table": table_name,
            "fields": list(T.__annotations__.keys()),
            "params": query_params,
        }
        results = self.do_query(**kwargs)

        # Create a list of objects to return
        list_of_objects = []
        for object in results:
            list_of_objects.append(T(**object))

        return list_of_objects
