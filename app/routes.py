"""
Flask API routes and endpoints.

Handles HTTP requests and responses only.
Business logic is delegated to services layer.
"""

from flask import Blueprint, request, jsonify
from typing import Tuple, Dict, Any

from app.services import add_user, get_user


api_bp = Blueprint('api', __name__)


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
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    if not isinstance(data['name'], str) or not data['name'].strip():
        return jsonify({"error": "Name must be a non-empty string"}), 400
    
    try:
        user_id = add_user(data['name'].strip())
        return jsonify({"id": user_id, "name": data['name'].strip()}), 201
    except Exception as e:
        return jsonify({"error": "Failed to create user"}), 500


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_endpoint(user_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Get user by ID endpoint.
    
    Args:
        user_id: User ID from URL path.
        
    Returns:
        JSON response with user data or error message and status code.
    """
    user = get_user(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user), 200


@api_bp.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, str], int]:
    """
    Health check endpoint.
    
    Returns:
        JSON response with service status.
    """
    return jsonify({"status": "healthy"}), 200

