"""
MongoDB document builder.
Constructs document structure for storage.
"""

from datetime import datetime
from typing import Dict, Any
from core.logging_config import logger


def build_yaml_document(
    filename: str,
    raw_yaml: str,
    parsed_yaml: Dict[str, Any],
    metadata: Dict[str, str],
    sections_count: int,
    sections: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Build MongoDB document from YAML data.
    
    Creates document with exact structure:
    {
        "filename": str,
        "raw_yaml": str,
        "parsed_yaml": dict,
        "metadata": {
            "name": str,
            "description": str,
            "version": str
        },
        "sections_count": int,
        "sections": dict,
        "uploaded_at": datetime
    }
    
    Args:
        filename: Original filename
        raw_yaml: Raw YAML content as string
        parsed_yaml: Parsed YAML as dictionary
        metadata: Metadata dict with name, description, version
        sections_count: Number of sections in YAML
        sections: Dictionary of sections
        
    Returns:
        Dict[str, Any]: MongoDB document ready for insertion
    """
    try:
        logger.info(f"Building MongoDB document for file: {filename}")
        
        document = {
            "filename": filename,
            "raw_yaml": raw_yaml,
            "parsed_yaml": parsed_yaml,
            "metadata": metadata,
            "sections_count": sections_count,
            "sections": sections,
            "uploaded_at": datetime.utcnow()
        }
        
        logger.info(f"Document built successfully with {sections_count} sections")
        return document
        
    except Exception as e:
        logger.error(f"Error building MongoDB document: {str(e)}")
        raise
