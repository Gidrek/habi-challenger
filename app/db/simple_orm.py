import logging
from re import T
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
        - filters: a list of filters to be applied
        - returning_fields: a list of the fields that need to be displayed
        """
        fields = ", ".join(kwargs["fields"])
        query = f"""SELECT {fields} from 
        {kwargs['table']}"""

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

        if T.__name__.lower()[-1] == "y":
            table_name = f"{T.__name__.lower()[:-1]}ies"
        else:
            table_name = f"{T.__name__.lower()}s"

        kwargs = {
            # For now, we are going to assume that the class is always plural with 'es'
            "table": table_name,
            "fields": list(T.__annotations__.keys()),
        }
        results = self.do_query(**kwargs)

        # Create a list of objects to return
        list_of_objects = []
        for object in results:
            list_of_objects.append(T(**object))

        return list_of_objects
