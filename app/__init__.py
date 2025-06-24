# app/__init__.py
from flask import Flask
from .routes import main as main_blueprint

def create_app():
    app = Flask(__name__, static_folder='static')

    # REQUIRED: Set a secret key for session management
    app.secret_key = "safeschool-super-secret-key"  # Replace with a more secure value for production

    # Register the routes from the main blueprint
    app.register_blueprint(main_blueprint)

    return app
