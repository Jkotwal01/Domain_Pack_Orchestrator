"""
Reasoning template Pydantic models.
Validates reasoning_templates section.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional


class ReasoningTemplateModel(BaseModel):
    """
    Model for reasoning template definition.
    
    Attributes:
        name: Template name (required)
        steps: Ordered steps as dict with numeric keys (required)
        triggers: List of trigger keywords (required)
        confidence_threshold: Minimum confidence threshold (required, 0-1)
    """
    name: str = Field(..., description="Template name")
    steps: Dict[str, str] = Field(..., description="Ordered reasoning steps")
    triggers: List[str] = Field(..., description="Trigger keywords")
    confidence_threshold: float = Field(
        ..., 
        description="Minimum confidence threshold (0-1)", 
        ge=0.0, 
        le=1.0
    )
    
    @field_validator('confidence_threshold')
    @classmethod
    def validate_confidence_threshold(cls, v: float) -> float:
        """
        Validate confidence threshold is between 0 and 1.
        
        Args:
            v: Confidence threshold value
            
        Returns:
            float: Validated confidence threshold
            
        Raises:
            ValueError: If threshold not in valid range
        """
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence threshold must be between 0.0 and 1.0')
        return v
