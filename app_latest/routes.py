"""
Flask API routes and endpoints.

Handles HTTP requests and responses only.
Business logic is delegated to services layer.
"""

import logging
import sqlite3
from flask import Blueprint, request, jsonify, current_app
from typing import Tuple, Dict, Any

from app_latest.services import add_user, get_user


logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)


def validate_name(name: Any, max_length: int = 255) -> Tuple[bool, Optional[str]]:
    """
    Validate user name.
    
    Args:
        name: Name to validate.
        max_length: Maximum allowed length.
        
    Returns:
        Tuple of (is_valid, error_message).
    """
    if not name:
        return False, "Name is required"
    
    if not isinstance(name, str):
        return False, "Name must be a string"
    
    name = name.strip()
    
    if not name:
        return False, "Name cannot be empty"
    
    if len(name) > max_length:
        return False, f"Name must be no longer than {max_length} characters"
    
    # Basic validation: no control characters
    if any(ord(c) < 32 and c not in '\t\n\r' for c in name):
        return False, "Name contains invalid characters"
    
    return True, None


@api_bp.route('/users', methods=['POST'])
def create_user() -> Tuple[Dict[str, Any], int]:
    """
    Create new user endpoint.
    
    Request body:
        {
            "name": "User Name"
        }
        
    Returns:
        JSON response with user data and status code.
    """
    # Validate Content-Type
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    # Validate request body size (prevent DoS)
    if request.content_length and request.content_length > 1024:
        return jsonify({"error": "Request body too large"}), 413
    
    try:
        data = request.get_json(force=False)
    except Exception as e:
        logger.warning(f"Invalid JSON in request: {e}")
        return jsonify({"error": "Invalid JSON format"}), 400
    
    if data is None:
        return jsonify({"error": "Request body is required"}), 400
    
    # Validate name
    if 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    max_length = current_app.config.get('MAX_NAME_LENGTH', 255)
    is_valid, error_msg = validate_name(data['name'], max_length)
    
    if not is_valid:
        return jsonify({"error": error_msg}), 400
    
    name = data['name'].strip()
    database_path = current_app.config['DATABASE_PATH']
    
    try:
        user_id = add_user(name, database_path)
        logger.info(f"User created successfully: ID={user_id}, name={name[:20]}")
        return jsonify({"id": user_id, "name": name}), 201
    
    except sqlite3.IntegrityError as e:
        logger.warning(f"Integrity error creating user: {e}")
        return jsonify({"error": "User with this name may already exist"}), 409
    
    except sqlite3.Error as e:
        logger.error(f"Database error creating user: {e}", exc_info=True)
        return jsonify({"error": "Database error occurred"}), 500
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_endpoint(user_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Get user by ID endpoint.
    
    Args:
        user_id: User ID from URL path.
        
    Returns:
        JSON response with user data or error message and status code.
    """
    if user_id <= 0:
        return jsonify({"error": "Invalid user ID"}), 400
    
    database_path = current_app.config['DATABASE_PATH']
    
    try:
        user = get_user(user_id, database_path)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user), 200
    
    except sqlite3.Error as e:
        logger.error(f"Database error getting user {user_id}: {e}", exc_info=True)
        return jsonify({"error": "Database error occurred"}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error getting user {user_id}: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.
    
    Returns:
        JSON response with service status.
    """
    try:
        # Basic health check - verify database is accessible
        database_path = current_app.config['DATABASE_PATH']
        from app_latest.database import get_db_connection
        
        with get_db_connection(database_path) as conn:
            conn.execute("SELECT 1")
        
        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200
    
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 503

