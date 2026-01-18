"""
Business-related Pydantic models.
Validates business_context, business_patterns, and business_rules sections.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class BusinessContextModel(BaseModel):
    """
    Model for business context configuration.
    
    Attributes:
        risk_levels: List of risk level values (optional)
        compliance_frameworks: List of compliance frameworks (optional)
        confidentiality_levels: List of confidentiality levels (optional)
        urgency_levels: List of urgency levels (optional)
    """
    risk_levels: Optional[List[str]] = Field(default=None, description="Risk level values")
    compliance_frameworks: Optional[List[str]] = Field(default=None, description="Compliance frameworks")
    confidentiality_levels: Optional[List[str]] = Field(default=None, description="Confidentiality levels")
    urgency_levels: Optional[List[str]] = Field(default=None, description="Urgency levels")
    
    class Config:
        """Pydantic configuration"""
        extra = "allow"  # Allow additional fields


class BusinessPatternModel(BaseModel):
    """
    Model for business pattern definition.
    
    Attributes:
        name: Pattern name (required)
        description: Pattern description (required)
        stages: List of workflow stages (optional)
        triggers: List of pattern triggers (optional)
        entities_involved: List of entity types involved (optional)
        tags: List of pattern tags (optional)
        decision_points: List of decision points (optional)
    """
    name: str = Field(..., description="Pattern name")
    description: str = Field(..., description="Pattern description")
    stages: Optional[List[str]] = Field(default=None, description="Workflow stages")
    triggers: Optional[List[str]] = Field(default=None, description="Pattern triggers")
    entities_involved: Optional[List[str]] = Field(default=None, description="Entity types involved")
    tags: Optional[List[str]] = Field(default=None, description="Pattern tags")
    decision_points: Optional[List[str]] = Field(default=None, description="Decision points")


class BusinessRuleModel(BaseModel):
    """
    Model for business rule definition.
    
    Attributes:
        name: Rule name (required)
        description: Rule description (required)
        rules: List of rule definitions (required, can be empty)
    """
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    rules: List[str] = Field(..., description="List of rule definitions")
