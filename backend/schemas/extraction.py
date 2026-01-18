"""
Extraction pattern Pydantic models.
Validates extraction_patterns section.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ExtractionPatternModel(BaseModel):
    """
    Model for extraction pattern definition.
    
    Attributes:
        pattern: Regex pattern for extraction (required)
        entity_type: Target entity type (required)
        attribute: Target attribute name (required)
        confidence: Confidence score between 0 and 1 (required)
    """
    pattern: str = Field(..., description="Regex pattern for extraction")
    entity_type: str = Field(..., description="Target entity type")
    attribute: str = Field(..., description="Target attribute name")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0.0, le=1.0)
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """
        Validate confidence is between 0 and 1.
        
        Args:
            v: Confidence value
            
        Returns:
            float: Validated confidence value
            
        Raises:
            ValueError: If confidence not in valid range
        """
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v
