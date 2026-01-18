"""
FastAPI application entry point.
Main application with MongoDB connection validation and route registration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from core.logging_config import logger
from db.connection import mongo_connection
from api.routes.upload import router as upload_router
from api.routes.validate import router as validate_router
from api.routes.list import router as list_router
from api.routes.intent import router as intent_router
from utils.error_handlers import (
    YAMLParseError,
    DatabaseError,
    yaml_parse_error_handler,
    database_error_handler,
    global_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    
    Startup:
    - Initialize logging
    - Connect to MongoDB with validation
    - Print success message to console
    
    Shutdown:
    - Close MongoDB connection gracefully
    """
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("=" * 60)
    
    # Connect to MongoDB
    connection_success = mongo_connection.connect()
    
    if not connection_success:
        logger.error("Failed to connect to MongoDB. Application may not function correctly.")
        print("\n⚠️  WARNING: MongoDB connection failed. Please ensure MongoDB is running.\n")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    mongo_connection.close()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise-grade backend for managing domain_config YAML files with MongoDB persistence and comprehensive validation",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register exception handlers
app.add_exception_handler(YAMLParseError, yaml_parse_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(Exception, global_exception_handler)


# Register routes
app.include_router(upload_router, tags=["YAML Management"])
app.include_router(validate_router, tags=["YAML Validation"])
app.include_router(list_router, tags=["YAML Management"])
app.include_router(intent_router, tags=["Intent Interpretation"])


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API health check.
    
    Returns:
        Dict with API status and information
    """
    logger.info("Health check endpoint called")
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "upload": "/upload - Upload and store YAML files",
            "validate": "/validate - Validate YAML structure without storing",
            "domain_pack_list": "/domain_pack_list - List all uploaded domain packs",
            "intent": "/intent - Convert natural language to structured intent",
            "docs": "/docs - Interactive API documentation"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Dict with health status
    """
    try:
        # Test MongoDB connection
        db = mongo_connection.get_database()
        db.command('ping')
        mongodb_status = "connected"
    except Exception as e:
        logger.error(f"MongoDB health check failed: {str(e)}")
        mongodb_status = "disconnected"
    
    return {
        "status": "healthy" if mongodb_status == "connected" else "degraded",
        "mongodb": mongodb_status,
        "service": settings.APP_NAME
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server with uvicorn...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
