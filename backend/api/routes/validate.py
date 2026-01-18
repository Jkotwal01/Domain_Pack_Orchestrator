"""
Validate endpoint.
Validates YAML structure without storing.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import Dict, Any
import yaml
from core.logging_config import logger
from services.yaml_parser import parse_yaml_content
from services.validation_service import validate_yaml_structure
from schemas.base import ValidationResult


router = APIRouter()


@router.post("/validate", status_code=status.HTTP_200_OK)
async def validate_yaml(file: UploadFile = File(...)) -> ValidationResult:
    """
    Validate YAML structure without storing.
    
    Process:
    1. Accept YAML file
    2. Parse YAML content
    3. Validate structure using Pydantic models
    4. Return validation result
    
    Args:
        file: Uploaded YAML file
        
    Returns:
        ValidationResult with exact format:
        {
            "is_valid": bool,
            "errors": [],      # Structural/required field violations
            "warnings": []     # Non-blocking issues
        }
        
    Raises:
        HTTPException: If file reading or parsing fails
    """
    try:
        logger.info(f"Received validation request for file: {file.filename}")
        
        # Validate file extension
        if not file.filename.endswith(('.yaml', '.yml')):
            logger.warning(f"Invalid file extension: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a YAML file (.yaml or .yml)"
            )
        
        # Read file content
        try:
            raw_yaml = await file.read()
            yaml_content = raw_yaml.decode('utf-8')
            logger.info(f"File read successfully: {len(yaml_content)} bytes")
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error reading file: {str(e)}"
            )
        
        # Parse YAML
        try:
            parsed_yaml = parse_yaml_content(yaml_content)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing failed: {str(e)}")
            # Return validation result with error instead of raising exception
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid YAML syntax: {str(e)}"],
                warnings=[]
            )
        except ValueError as e:
            logger.error(f"YAML structure error: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[str(e)],
                warnings=[]
            )
        
        # Validate structure
        try:
            validation_result = validate_yaml_structure(parsed_yaml)
            
            if validation_result.is_valid:
                logger.info(f"Validation passed for {file.filename}")
            else:
                logger.warning(
                    f"Validation failed for {file.filename}: "
                    f"{len(validation_result.errors)} errors, "
                    f"{len(validation_result.warnings)} warnings"
                )
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[]
            )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in validate endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
