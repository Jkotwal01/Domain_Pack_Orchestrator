"""
Custom error handlers and exception classes.
Provides user-friendly error responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.logging_config import logger
from typing import Any, Dict


class YAMLParseError(Exception):
    """Exception raised for YAML parsing errors"""
    pass


class ValidationError(Exception):
    """Exception raised for validation errors"""
    pass


class DatabaseError(Exception):
    """Exception raised for database errors"""
    pass


async def yaml_parse_error_handler(request: Request, exc: YAMLParseError) -> JSONResponse:
    """
    Handle YAML parsing errors.
    
    Args:
        request: FastAPI request
        exc: YAMLParseError exception
        
    Returns:
        JSONResponse: Error response
    """
    logger.error(f"YAML parse error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "YAML Parsing Error",
            "message": str(exc),
            "detail": "The uploaded file contains invalid YAML syntax"
        }
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """
    Handle database errors.
    
    Args:
        request: FastAPI request
        exc: DatabaseError exception
        
    Returns:
        JSONResponse: Error response
    """
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "An error occurred while accessing the database",
            "detail": "Please check if MongoDB is running and accessible"
        }
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: FastAPI request
        exc: Exception
        
    Returns:
        JSONResponse: Error response
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": "Please check the logs for more information"
        }
    )
