"""
Application entry point.

Creates Flask application instance and runs development server.
For production, use Gunicorn: gunicorn --bind 0.0.0.0:8000 main:app
"""

from app import create_app


app = create_app()


if __name__ == "__main__":
    # Only for development
    # Production should use Gunicorn
    app.run(host="0.0.0.0", port=8000, debug=False)

