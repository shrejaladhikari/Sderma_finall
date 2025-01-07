# app/__init__.py
from flask import Flask
from .routes import main
from .db import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"

    # Register the Blueprint for routes
    app.register_blueprint(main)

    # Initialize the database
    init_db()

    return app