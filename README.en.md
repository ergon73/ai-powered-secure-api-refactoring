# Flask Security Refactoring Project

[🇷🇺 Русский](README.md) | [🇬🇧 English](README.en.md)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Project Overview

Production-ready Flask API demonstrating security best practices and modern Python development. This project was refactored from legacy vulnerable code to a secure, maintainable, and well-documented application.

## 🔒 Security Improvements

### Before (Vulnerabilities Found)

| Issue | Severity | Location |
|-------|----------|----------|
| SQL Injection | 🔴 Critical | `api.py`, `utils.py` |
| Plaintext Passwords | 🔴 Critical | `utils.py:store_password()` |
| Race Conditions | 🟡 High | `utils.py:active_users` |
| Resource Leaks | 🟡 High | Unclosed DB connections |
| No Type Hints | 🟢 Medium | All files |
| PEP 8 Violations | 🟢 Medium | All files |

### After (Fixed)

✅ **Parameterized SQL queries** prevent injection attacks  
✅ **PBKDF2 password hashing** with salt (Werkzeug)  
✅ **Thread-safe operations** with locks  
✅ **Context managers** for resource management  
✅ **Full type hints** (PEP 484)  
✅ **PEP 8 compliance** throughout codebase  
✅ **Correct HTTP status codes** (200, 201, 404, 400, 500)  
✅ **Modular architecture** with separation of concerns  

## 🏗️ Architecture

### Project Versions

The project contains two versions:

1. **`app/`** — Basic refactored version
   - All critical security vulnerabilities fixed
   - Modular architecture
   - Basic error handling

2. **`app_latest/`** — Improved version with audit fixes ⭐ **Recommended**
   - All fixes from basic version
   - Enhanced error handling with logging
   - Configuration via environment variables
   - Full input validation
   - Fixed `init_db` issue with Gunicorn
   - Updated OpenAPI with all error descriptions
   - See `app_latest/README.md` for details

```
Modular Flask Application
├── app/               # Basic version
│   ├── __init__.py    # Flask app factory
│   ├── database.py    # DB connection management
│   ├── routes.py      # API endpoints (blueprints)
│   ├── services.py    # Business logic layer
│   └── security.py    # Password hashing & validation
├── app_latest/        # Improved version ⭐
│   ├── __init__.py    # Flask factory with env config
│   ├── config.py      # Configuration management
│   ├── database.py    # DB with logging
│   ├── routes.py      # Endpoints with full validation
│   ├── services.py    # Business logic with error handling
│   ├── security.py    # Password hashing
│   └── README.md      # Improvements documentation
├── main.py            # Entry point (basic version)
├── main-latest.py     # Entry point (improved version) ⭐
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container configuration
├── openapi.yaml       # API documentation (basic)
├── openapi-latest.yaml # API documentation (improved) ⭐
└── README.md          # Project documentation
```

### Design Principles

- **Separation of Concerns**: Routes handle HTTP only, services contain business logic
- **Security First**: All SQL queries use parameterized statements
- **Resource Management**: Context managers ensure proper cleanup
- **Thread Safety**: Shared state protected with locks
- **Type Safety**: Complete type hints for better maintainability

## 🚀 Quick Start

### Local Development

#### Basic Version (`app/`)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

#### Improved Version (`app_latest/`) ⭐ **Recommended**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run improved version
python main-latest.py

# Or with environment variables
export DATABASE_PATH=my_app.db
export MAX_NAME_LENGTH=100
export LOG_LEVEL=DEBUG
python main-latest.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

```bash
# Build image
docker build -t flask-security-api:latest .

# Run container
docker run -p 8000:8000 flask-security-api:latest

# Test health endpoint
curl http://localhost:8000/health
```

## 📡 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| POST | `/users` | Create new user | 201, 400, 500 |
| GET | `/users/{id}` | Get user by ID | 200, 404 |
| GET | `/health` | Health check | 200 |

Full API documentation:
- Basic version: `openapi.yaml`
- Improved version: `openapi-latest.yaml` ⭐

### Example Requests

**Create User:**
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

**Get User:**
```bash
curl http://localhost:8000/users/1
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

## 🧪 Testing

### Manual Testing

```bash
# Create user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User"}'

# Get user (replace 1 with actual user ID)
curl http://localhost:8000/users/1

# Test error handling - invalid request
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{}'

# Test error handling - not found
curl http://localhost:8000/users/999
```

### Using Postman/Insomnia

Import `openapi.yaml` (basic version) or `openapi-latest.yaml` (improved version) file to get all endpoints pre-configured.

## 📦 Tech Stack

- **Framework:** Flask 3.0.0
- **WSGI Server:** Gunicorn 21.2.0
- **Database:** SQLite (production should use PostgreSQL/MySQL)
- **Security:** Werkzeug password hashing (PBKDF2-SHA256)
- **Python:** 3.11+

## 🔐 Security Features

1. **SQL Injection Prevention**
   - All queries use parameterized statements with `?` placeholders
   - No string formatting or concatenation in SQL

2. **Password Security**
   - PBKDF2 with SHA-256 and salt
   - No plaintext storage or reversible "encryption"

3. **Thread Safety**
   - Shared mutable state protected with `threading.Lock()`
   - No race conditions in concurrent operations

4. **Resource Management**
   - Context managers for database connections
   - Automatic cleanup on errors

5. **Input Validation**
   - Request validation in route handlers
   - Type checking and sanitization

## 🐳 Docker Configuration

The Dockerfile follows production best practices:

- ✅ Lightweight base image (`python:3.11-slim`)
- ✅ Non-root user for security
- ✅ Layer caching optimization
- ✅ Gunicorn production server (not Flask dev server)
- ✅ Health check for container orchestration
- ✅ Proper signal handling

## 📚 Code Quality

- **Type Hints:** All functions have complete type annotations (PEP 484)
- **PEP 8:** Strict compliance with Python style guide
- **Docstrings:** Google-style documentation for all public functions
- **Error Handling:** Specific exception handling with proper HTTP status codes
- **Architecture:** Modular design with clear separation of concerns

## 🤖 AI-Assisted Development

This project was refactored using AI-powered tools (Cursor IDE) following best practices for:
- Prompt engineering
- Code quality standards
- Security-first development
- Modern Python patterns

## 📄 License

MIT License - see LICENSE file

## 👤 Author

**Georgy Belyanin (Георгий Белянин)**  
📧 georgy.belyanin@gmail.com

Portfolio Project - Security Refactoring Demonstration

---

## 📊 Version Comparison

| Feature | `app/` | `app_latest/` ⭐ |
|---------|--------|-----------------|
| Security (SQL injection, passwords) | ✅ | ✅ |
| Modular architecture | ✅ | ✅ |
| Error handling | Basic | Enhanced with logging |
| Configuration | Hardcoded | Via environment variables |
| Input validation | Minimal | Full (type, length, characters) |
| Logging | None | Configurable |
| init_db in Gunicorn | Issue | Fixed |
| OpenAPI specification | Basic | Complete with error descriptions |
| Health check | Simple | With DB check |

**Recommendation:** Use `app_latest/` for new projects and production.

---

**Note:** This is a demonstration project. For production use, consider:
- Using PostgreSQL or MySQL instead of SQLite
- Adding authentication and authorization
- Implementing rate limiting
- Adding comprehensive test suite
- Setting up CI/CD pipeline
- Using environment variables for configuration (implemented in `app_latest/`)
- Adding logging and monitoring (implemented in `app_latest/`)

