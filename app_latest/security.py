"""
Password hashing and verification utilities.

Implements secure password storage using PBKDF2 with SHA-256.
Note: Currently not used in API endpoints, but available for future use.
"""

from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2 with salt.
    
    Args:
        password: Plain text password to hash.
        
    Returns:
        Hashed password string.
    """
    return generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=16
    )


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify password against hash.
    
    Args:
        password_hash: Stored password hash.
        password: Plain text password to verify.
        
    Returns:
        True if password matches hash, False otherwise.
    """
    return check_password_hash(password_hash, password)

