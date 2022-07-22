"""
Simple server to access through HTTPS, this generate a JSON response
"""
import sys
import json
import logging
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer

from settings.settings import Settings
from db.simple_orm import SimpleORM

from models.property import Property


class RunServer:
    """Class to run the SimpleServer interface"""

    def __init__(self) -> None:
        """Initialize the server with hostname and port

        This constructor set the logging level to INFO to log to console
        """
        settings = Settings()
        logging.basicConfig(level=logging.INFO)
        self.server = HTTPServer((settings.hostname, settings.port), SimpleServer)
        logging.info(f"Server started http://{settings.hostname}:{settings.port}")

    def run(self) -> None:
        """Runs the server in a infinite loop until interrup with the keyboard"""
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
            logging.info("Server stopped successfully")
            sys.exit(0)


class SimpleServer(BaseHTTPRequestHandler):
    """SimpleServer class. This only accepts GET method with query params optional"""

    def do_GET(self) -> None:
        """Serve a GET request."""

        path_with_query = self.path.split("?")
        path = path_with_query[0]
        query = ""
        if len(path_with_query) > 1:
            query = path_with_query[1]

        if path == "/":
            # When got the root of the server, only response with JSON hello world
            self.send_response(200, "OK")
            self.send_header("Content-type", "application/json")
            self.end_headers()

            hello_dict = {"hello": "world"}

            self.wfile.write(bytes(json.dumps(hello_dict), "utf-8"))

        if path == "/properties/":
            # Need to clean params
            params = urllib.parse.parse_qs(query)

            # For now, we are going to connecting here
            logging.info("Connecting to database ....")
            orm = SimpleORM()
            logging.info("Connecting to database successfully ....")

            # Response from the server
            self.send_response(200, "OK")
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # We use our ORM to get the objects
            properties = orm.get_objects(Property, **params)

            # We only get some fields from the property
            returning_objects = []
            for property in properties:
                # If there is not info about price or address, then we don't add to the list of
                # objects
                if property.price == 0 or not property.address or not property.city:
                    continue

                pro = {
                    "address": property.address,
                    "city": property.city,
                    "price": property.price,
                    "description": property.description,
                }
                returning_objects.append(pro)

            self.wfile.write(bytes(json.dumps(returning_objects), "utf-8"))
