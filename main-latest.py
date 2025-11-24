"""
Application entry point (improved version).

Creates Flask application instance and runs development server.
For production, use Gunicorn: gunicorn --bind 0.0.0.0:8000 main_latest:app

Environment variables:
    DATABASE_PATH: Path to SQLite database (default: secure_app.db)
    DEBUG: Enable debug mode (default: False)
    MAX_NAME_LENGTH: Maximum user name length (default: 255)
    INIT_DB_ON_START: Initialize DB on startup (default: True)
    LOG_LEVEL: Logging level (default: INFO)
"""

import logging
import sys
from app_latest import create_app
from app_latest.config import get_config


# Configure logging
config = get_config()
logging.basicConfig(
    level=getattr(logging, config['LOG_LEVEL'], logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    # Only for development
    # Production should use Gunicorn
    logger.info("Starting Flask development server...")
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=config['DEBUG']
    )

