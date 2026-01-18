# Domain Config Backend

Enterprise-grade FastAPI backend for managing domain_config YAML files with MongoDB persistence and comprehensive validation.

## Features

- ✅ **MongoDB Integration** - Persistent storage with startup validation
- ✅ **Pydantic v2 Validation** - 14 comprehensive models for strict YAML validation
- ✅ **REST API** - Two endpoints: `/upload` (store) and `/validate` (validate only)
- ✅ **Structured Logging** - Dual output (console + file) with detailed tracking
- ✅ **Error Handling** - Comprehensive try-catch blocks with user-friendly messages
- ✅ **Production Ready** - Scalable architecture, maintainable code, full documentation

## Quick Start

### Prerequisites

- Python 3.8+
- MongoDB running on `localhost:27017`

### Installation

```bash
cd d:/Anti/backend
pip install -r requirements.txt
```

### Start Server

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: http://localhost:8000

### API Documentation

Interactive Swagger UI: http://localhost:8000/docs

## API Endpoints

### POST /upload

Upload and persist YAML file to MongoDB.

**Request**: Multipart form data with YAML file

**Response**:
```json
{
    "document_id": "696c9efbd18d6e86cb6ac1a4",
    "filename": "sample.yaml",
    "metadata": {
        "name": "Legal",
        "description": "Legal and compliance domain",
        "version": "3.0.0"
    },
    "sections_count": 13,
    "message": "YAML file uploaded successfully"
}
```

### POST /validate

Validate YAML structure without storing.

**Request**: Multipart form data with YAML file

**Response**:
```json
{
    "is_valid": true,
    "errors": [],
    "warnings": []
}
```

### GET /health

Health check endpoint.

**Response**:
```json
{
    "status": "healthy",
    "mongodb": "connected",
    "service": "Domain Config Backend"
}
```

## Project Structure

```
backend/
├── api/routes/          # REST endpoints
├── core/                # Configuration and logging
├── db/                  # MongoDB connection
├── models/              # Document builders
├── schemas/             # Pydantic validation models
├── services/            # Business logic
├── utils/               # Error handlers
├── logs/                # Application logs
└── main.py              # FastAPI application
```

## Configuration

Create `.env` file (optional):

```env
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=domain_config_db
COLLECTION_NAME=yaml_configs
LOG_FILE_PATH=logs/app.log
LOG_LEVEL=INFO
```

## Testing

### Test MongoDB Connection

```bash
python test_connection.py
```

### Test All Endpoints

```bash
python test_endpoints.py
```

## Supported YAML Sections

The backend validates and stores the following sections:

- **Required**: name, description, version
- **Optional**: entities, key_terms, entity_aliases, extraction_patterns, business_context, relationship_types, relationships, business_patterns, reasoning_templates, multihop_questions, question_templates, business_rules, validation_rules

## Logging

All logs are written to:
- **Console**: INFO level and above
- **File**: `logs/app.log` - DEBUG level and above

Log format: `timestamp | level | module | message`

## MongoDB Document Structure

```python
{
    "filename": str,
    "raw_yaml": str,
    "parsed_yaml": dict,
    "metadata": {
        "name": str,
        "description": str,
        "version": str
    },
    "sections_count": int,
    "sections": dict,
    "uploaded_at": datetime
}
```

## Error Handling

All errors are:
- Logged to `logs/app.log`
- Returned as JSON with user-friendly messages
- Never expose raw stack traces

## Dependencies

- fastapi - Web framework
- uvicorn - ASGI server
- pymongo - MongoDB driver
- pydantic - Data validation
- pydantic-settings - Configuration management
- pyyaml - YAML parsing
- python-multipart - File upload support

## License

MIT

## Author

Built with enterprise-grade standards for production use.
