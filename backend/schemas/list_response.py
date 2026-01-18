"""
Response schemas for domain pack list endpoint.
"""

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class DomainPackListItem(BaseModel):
    """
    Model for individual domain pack in the list.
    
    Attributes:
        domain_pack_id: MongoDB document ID as string
        domain_name: Name of the domain from metadata
        description: Description of the domain from metadata
        uploaded_at: Timestamp when the domain pack was uploaded
    """
    domain_pack_id: str = Field(..., description="Unique identifier for the domain pack")
    domain_name: str = Field(..., description="Name of the domain")
    description: str = Field(..., description="Description of the domain")
    uploaded_at: datetime = Field(..., description="Upload timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DomainPackListResponse(BaseModel):
    """
    Response model for domain pack list endpoint.
    
    Attributes:
        total_count: Total number of domain packs in the database
        domain_packs: List of domain pack summary items
    """
    total_count: int = Field(..., description="Total number of domain packs")
    domain_packs: List[DomainPackListItem] = Field(..., description="List of domain packs")
