"""
Base Pydantic models for domain config validation.
Contains metadata and validation result models.
"""

from pydantic import BaseModel, Field
from typing import List


class MetadataModel(BaseModel):
    """
    Metadata model for domain config.
    All fields are required.
    """
    name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    version: str = Field(..., description="Domain version")


class ValidationResult(BaseModel):
    """
    Validation result model returned by /validate endpoint.
    
    Attributes:
        is_valid: True if validation passed, False otherwise
        errors: List of structural or required field violations
        warnings: List of non-blocking issues (e.g., empty lists)
    """
    is_valid: bool = Field(..., description="Whether validation passed")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
