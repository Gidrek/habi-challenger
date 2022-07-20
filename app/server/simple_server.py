"""
Simple server to access through HTTPS, this generate a JSON response
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


HOSTNAME = os.environ.get("HOSTNAME", "localhost")
PORT = os.environ.get("PORT", 8000)


class RunServer:
    """Class to run the SimpleServer interface"""

    def __init__(self) -> None:
        """Initialize the server with hostname and port"""
        self.server = HTTPServer((HOSTNAME, PORT), SimpleServer)
        print(f"Server started http://{HOSTNAME}:{PORT}")

    def run(self) -> None:
        """Runs the server in a infinite loop until interrup with the keyboard"""
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.server_close()
            print("Server stopped successfully")
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
