"""
Upload endpoint.
Handles YAML file upload and storage in MongoDB.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import Dict, Any
import yaml
from core.logging_config import logger
from db.connection import get_collection
from services.yaml_parser import parse_yaml_content, extract_metadata, count_sections, convert_numeric_keys_to_strings
from models.document import build_yaml_document
from utils.error_handlers import YAMLParseError, DatabaseError


router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_yaml(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and persist a domain_config YAML file.
    
    Process:
    1. Accept YAML file
    2. Perform basic validation (valid YAML, required fields)
    3. Parse YAML into Python dict
    4. Store in MongoDB with metadata
    
    Args:
        file: Uploaded YAML file
        
    Returns:
        Dict containing:
        - document_id: MongoDB document ID
        - filename: Original filename
        - metadata: Extracted metadata (name, description, version)
        - sections_count: Number of sections
        - message: Success message
        
    Raises:
        HTTPException: If validation or storage fails
    """
    try:
        logger.info(f"Received upload request for file: {file.filename}")
        
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid YAML syntax: {str(e)}"
            )
        
        # Extract metadata
        try:
            metadata = extract_metadata(parsed_yaml)
        except KeyError as e:
            logger.error(f"Missing required metadata: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Count sections
        try:
            sections_count, sections = count_sections(parsed_yaml)
        except Exception as e:
            logger.error(f"Error counting sections: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing YAML structure: {str(e)}"
            )
        
        # Convert numeric keys to strings for MongoDB compatibility
        try:
            parsed_yaml = convert_numeric_keys_to_strings(parsed_yaml)
            sections = convert_numeric_keys_to_strings(sections)
            logger.info("Converted numeric keys to strings for MongoDB compatibility")
        except Exception as e:
            logger.error(f"Error converting keys: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error preparing data for storage: {str(e)}"
            )
        
        # Build MongoDB document
        try:
            document = build_yaml_document(
                filename=file.filename,
                raw_yaml=yaml_content,
                parsed_yaml=parsed_yaml,
                metadata=metadata,
                sections_count=sections_count,
                sections=sections
            )
        except Exception as e:
            logger.error(f"Error building document: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error building document: {str(e)}"
            )
        
        # Store in MongoDB
        try:
            collection = get_collection()
            result = collection.insert_one(document)
            document_id = str(result.inserted_id)
            logger.info(f"Document stored successfully with ID: {document_id}")
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error storing document in database. Please ensure MongoDB is running."
            )
        
        # Return success response
        response = {
            "document_id": document_id,
            "filename": file.filename,
            "metadata": metadata,
            "sections_count": sections_count,
            "message": f"YAML file '{file.filename}' uploaded and stored successfully"
        }
        
        logger.info(f"Upload completed successfully for {file.filename}")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in upload endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
