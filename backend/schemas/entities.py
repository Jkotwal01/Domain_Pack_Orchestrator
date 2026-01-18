"""
Entity-related Pydantic models.
Validates entities and entity aliases sections.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class EntityModel(BaseModel):
    """
    Model for individual entity definition.
    
    Attributes:
        name: Entity name (required)
        type: Entity type identifier (required)
        attributes: List of entity attributes (required, can be empty)
        synonyms: List of entity synonyms (optional, can be empty)
    """
    name: str = Field(..., description="Entity name")
    type: str = Field(..., description="Entity type identifier")
    attributes: List[str] = Field(..., description="List of entity attributes")
    synonyms: Optional[List[str]] = Field(default=None, description="List of entity synonyms")


class EntityAliasesModel(BaseModel):
    """
    Model for entity aliases mapping.
    Maps entity type to list of aliases.
    
    Example:
        {
            "CLIENT": ["customer", "party"],
            "ATTORNEY": ["lawyer", "counsel"]
        }
    """
    model_config = {"extra": "allow"}  # Pydantic v2 config
    
    # This will accept any dict structure
    # We'll validate it's Dict[str, List[str]] at runtime if needed
