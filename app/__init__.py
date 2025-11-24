"""
Flask Application Factory.

Creates and configures the Flask application instance.
"""

from flask import Flask
from typing import Any


def create_app() -> Flask:
    """
    Create and configure Flask application instance.
    
    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Initialize database
    from app.database import init_db
    init_db()
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app

