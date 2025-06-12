# app/__init__.py
from flask import Flask
from .routes import main as main_blueprint  # Correct relative import

def create_app():
    app = Flask(__name__)

    # Register the routes from the main blueprint
    app.register_blueprint(main_blueprint)

    return app
