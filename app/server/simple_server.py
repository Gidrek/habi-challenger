"""
Simple server to access through HTTPS, this generate a JSON response
"""
import sys
import json
import logging
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

        if self.path == "/":
            # When got the root of the server, only response with JSON hello world
            self.send_response(200, "OK")
            self.send_header("Content-type", "application/json")
            self.end_headers()

            hello_dict = {"hello": "world"}

            self.wfile.write(bytes(json.dumps(hello_dict), "utf-8"))

        if self.path == "/properties/":
            # For now, we are going to connecting here
            logging.info("Connecting to database ....")
            orm = SimpleORM()
            logging.info("Connecting to database successfully ....")

            self.send_response(200, "OK")
            self.send_header("Content-type", "application/json")
            self.end_headers()

            properties = orm.get_objects(Property)

            # We only get some fields from the property
            returning_objects = []
            for property in properties:
                pro = {
                    "address": property.address,
                    "city": property.city,
                    "state": property.state,
                    "price": property.price,
                    "description": property.description,
                }
                returning_objects.append(pro)

            self.wfile.write(bytes(json.dumps(returning_objects), "utf-8"))
