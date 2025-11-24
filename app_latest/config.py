"""
Configuration management.

Loads configuration from environment variables with sensible defaults.
"""

import os
from typing import Dict, Any


def get_config() -> Dict[str, Any]:
    """
    Get application configuration from environment variables.
    
    Returns:
        Dictionary with configuration values.
    """
    return {
        'DATABASE_PATH': os.getenv('DATABASE_PATH', 'secure_app.db'),
        'DEBUG': os.getenv('DEBUG', 'False').lower() == 'true',
        'MAX_NAME_LENGTH': int(os.getenv('MAX_NAME_LENGTH', '255')),
        'INIT_DB_ON_START': os.getenv('INIT_DB_ON_START', 'True').lower() == 'true',
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
    }
