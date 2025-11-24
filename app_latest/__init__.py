"""
Flask Application Factory.

Creates and configures the Flask application instance.
"""

import logging
import os
from flask import Flask
from typing import Any

from app_latest.config import get_config


logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Create and configure Flask application instance.
    
    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Load configuration from environment
    config = get_config()
    app.config.update(config)
    
    # Initialize database only once (not per worker)
    # In production with Gunicorn, init_db should be called separately
    # before starting workers, or use a migration system
    if config['INIT_DB_ON_START']:
        try:
            from app_latest.database import init_db
            init_db(config['DATABASE_PATH'])
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            # In production, you might want to fail fast here
            if not config['DEBUG']:
                raise
    
    # Register blueprints
    from app_latest.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
