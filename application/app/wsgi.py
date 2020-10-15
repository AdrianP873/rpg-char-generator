"""
This module is the WSGI entrypoint to the application.
"""

from app import app

if __name__ == "__main__":
    app.run()
