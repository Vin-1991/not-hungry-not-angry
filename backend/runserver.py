"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from os import environ
from app import app

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    HOST = environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(environ.get("SERVER_PORT", "5000"))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug=True, use_reloader=True)
