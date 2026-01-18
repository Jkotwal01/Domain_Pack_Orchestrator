"""
Relationship Pydantic models.
Validates relationships and relationship_types sections.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class RelationshipModel(BaseModel):
    """
    Model for relationship definition.
    
    Attributes:
        name: Relationship name (required)
        from_: Source entity type (required, mapped from 'from')
        to: Target entity type (required)
        attributes: List of relationship attributes (required, can be empty)
        synonyms: List of relationship synonyms (optional, can be empty)
    """
    name: str = Field(..., description="Relationship name")
    from_: str = Field(..., alias="from", description="Source entity type")
    to: str = Field(..., description="Target entity type")
    attributes: List[str] = Field(..., description="List of relationship attributes")
    synonyms: Optional[List[str]] = Field(default=None, description="List of relationship synonyms")
    
    class Config:
        """Pydantic configuration"""
        populate_by_name = True  # Allow both 'from' and 'from_'


class RelationshipTypeModel(BaseModel):
    """
    Model for relationship type definition.
    
    Attributes:
        type: Relationship type identifier (required)
        business_context: Business context metadata (required)
    """
    type: str = Field(..., description="Relationship type identifier")
    business_context: Dict[str, Any] = Field(..., description="Business context metadata")
