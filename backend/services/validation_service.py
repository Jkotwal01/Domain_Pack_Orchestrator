"""
Validation service.
Handles YAML structure validation using Pydantic models.
"""

from typing import Dict, Any, List, Tuple
from pydantic import ValidationError
from schemas.domain_config import DomainConfigModel
from schemas.base import ValidationResult
from core.logging_config import logger


def validate_yaml_structure(parsed_yaml: Dict[str, Any]) -> ValidationResult:
    """
    Validate YAML structure using Pydantic models.
    
    Args:
        parsed_yaml: Parsed YAML dictionary
        
    Returns:
        ValidationResult: Validation result with errors and warnings
    """
    try:
        logger.info("Starting YAML structure validation")
        
        errors: List[str] = []
        warnings: List[str] = []
        
        # Attempt to validate using Pydantic model
        try:
            domain_config = DomainConfigModel(**parsed_yaml)
            logger.info("YAML structure validation passed")
            
            # Check for warnings (e.g., empty lists)
            warnings = check_for_warnings(parsed_yaml)
            
            return ValidationResult(
                is_valid=True,
                errors=[],
                warnings=warnings
            )
            
        except ValidationError as e:
            logger.warning(f"YAML validation failed: {e.error_count()} errors found")
            
            # Extract and format validation errors
            for error in e.errors():
                field_path = " -> ".join(str(loc) for loc in error['loc'])
                error_msg = f"{field_path}: {error['msg']}"
                errors.append(error_msg)
                logger.debug(f"Validation error: {error_msg}")
            
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings
            )
            
    except Exception as e:
        logger.error(f"Unexpected error during validation: {str(e)}")
        return ValidationResult(
            is_valid=False,
            errors=[f"Validation error: {str(e)}"],
            warnings=[]
        )


def check_for_warnings(parsed_yaml: Dict[str, Any]) -> List[str]:
    """
    Check for non-blocking issues that should be warned about.
    
    Args:
        parsed_yaml: Parsed YAML dictionary
        
    Returns:
        List[str]: List of warning messages
    """
    warnings: List[str] = []
    
    try:
        # Check for empty lists in key sections
        list_sections = [
            'entities', 'key_terms', 'extraction_patterns', 
            'relationships', 'business_patterns', 'business_rules'
        ]
        
        for section in list_sections:
            if section in parsed_yaml:
                if isinstance(parsed_yaml[section], list) and len(parsed_yaml[section]) == 0:
                    warnings.append(f"Section '{section}' is present but empty")
        
        # Check for empty entity_aliases
        if 'entity_aliases' in parsed_yaml:
            if isinstance(parsed_yaml['entity_aliases'], dict) and len(parsed_yaml['entity_aliases']) == 0:
                warnings.append("Section 'entity_aliases' is present but empty")
        
        if warnings:
            logger.info(f"Found {len(warnings)} warnings")
        
    except Exception as e:
        logger.error(f"Error checking for warnings: {str(e)}")
    
    return warnings


def format_validation_errors(errors: List[str]) -> str:
    """
    Format validation errors into a readable string.
    
    Args:
        errors: List of error messages
        
    Returns:
        str: Formatted error message
    """
    if not errors:
        return "No errors"
    
    formatted = "Validation errors:\n"
    for i, error in enumerate(errors, 1):
        formatted += f"  {i}. {error}\n"
    
    return formatted.strip()
