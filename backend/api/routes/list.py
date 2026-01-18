"""
List endpoint.
Handles retrieval of all uploaded domain packs from MongoDB.
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from core.logging_config import logger
from db.connection import get_collection
from schemas.list_response import DomainPackListResponse, DomainPackListItem


router = APIRouter()


@router.get("/domain_pack_list", response_model=DomainPackListResponse)
async def get_domain_pack_list() -> DomainPackListResponse:
    """
    Retrieve all uploaded domain packs from MongoDB.
    
    Returns a list of all domain configurations that have been uploaded,
    sorted by upload time with the most recent first.
    
    Returns:
        DomainPackListResponse containing:
        - total_count: Total number of domain packs
        - domain_packs: List of domain pack summaries with:
            - domain_pack_id: MongoDB document ID
            - domain_name: Name from metadata
            - description: Description from metadata
            - uploaded_at: Upload timestamp
    
    Raises:
        HTTPException: If database query fails
    """
    try:
        logger.info("Fetching domain pack list from database")
        
        # Get MongoDB collection
        collection = get_collection()
        
        # Query all documents, projecting only required fields
        # Sort by uploaded_at descending (most recent first)
        cursor = collection.find(
            {},  # No filter - get all documents
            {
                "_id": 1,
                "metadata.name": 1,
                "metadata.description": 1,
                "uploaded_at": 1
            }
        ).sort("uploaded_at", -1)  # -1 for descending order
        
        # Convert cursor to list
        documents = list(cursor)
        
        logger.info(f"Retrieved {len(documents)} domain packs from database")
        
        # Build response
        domain_packs = []
        for doc in documents:
            domain_pack = DomainPackListItem(
                domain_pack_id=str(doc["_id"]),
                domain_name=doc["metadata"]["name"],
                description=doc["metadata"]["description"],
                uploaded_at=doc["uploaded_at"]
            )
            domain_packs.append(domain_pack)
        
        response = DomainPackListResponse(
            total_count=len(domain_packs),
            domain_packs=domain_packs
        )
        
        logger.info(f"Successfully built response with {response.total_count} domain packs")
        return response
        
    except Exception as e:
        logger.error(f"Error fetching domain pack list: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving domain pack list: {str(e)}"
        )
