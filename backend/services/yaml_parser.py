"""
YAML parsing service.
Handles YAML file parsing and metadata extraction.
"""

import yaml
from typing import Dict, Any, Tuple
from core.logging_config import logger


def parse_yaml_content(yaml_content: str) -> Dict[str, Any]:
    """
    Parse YAML string to Python dictionary.
    
    Args:
        yaml_content: YAML content as string
        
    Returns:
        Dict[str, Any]: Parsed YAML as dictionary
        
    Raises:
        yaml.YAMLError: If YAML parsing fails
        Exception: For other unexpected errors
    """
    try:
        logger.info("Parsing YAML content")
        parsed_data = yaml.safe_load(yaml_content)
        
        if parsed_data is None:
            logger.warning("YAML content is empty")
            return {}
        
        if not isinstance(parsed_data, dict):
            logger.error(f"YAML root must be a dictionary, got {type(parsed_data)}")
            raise ValueError("YAML root must be a dictionary")
        
        logger.info("YAML parsed successfully")
        return parsed_data
        
    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error parsing YAML: {str(e)}")
        raise


def extract_metadata(parsed_yaml: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract metadata (name, description, version) from parsed YAML.
    
    Args:
        parsed_yaml: Parsed YAML dictionary
        
    Returns:
        Dict[str, str]: Metadata dictionary with name, description, version
        
    Raises:
        KeyError: If required metadata fields are missing
    """
    try:
        logger.info("Extracting metadata from YAML")
        
        required_fields = ['name', 'description', 'version']
        missing_fields = [field for field in required_fields if field not in parsed_yaml]
        
        if missing_fields:
            error_msg = f"Missing required metadata fields: {', '.join(missing_fields)}"
            logger.error(error_msg)
            raise KeyError(error_msg)
        
        metadata = {
            'name': str(parsed_yaml['name']),
            'description': str(parsed_yaml['description']),
            'version': str(parsed_yaml['version'])
        }
        
        logger.info(f"Metadata extracted: {metadata['name']} v{metadata['version']}")
        return metadata
        
    except KeyError as e:
        logger.error(f"Metadata extraction error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error extracting metadata: {str(e)}")
        raise


def count_sections(parsed_yaml: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """
    Count and identify sections in the YAML.
    
    Args:
        parsed_yaml: Parsed YAML dictionary
        
    Returns:
        Tuple[int, Dict[str, Any]]: (section count, sections dict)
    """
    try:
        logger.info("Counting YAML sections")
        
        # Define all possible sections (excluding metadata)
        section_keys = [
            'entities', 'key_terms', 'entity_aliases', 'extraction_patterns',
            'business_context', 'relationship_types', 'relationships',
            'business_patterns', 'reasoning_templates', 'multihop_questions',
            'question_templates', 'business_rules', 'validation_rules'
        ]
        
        # Extract present sections
        sections = {}
        for key in section_keys:
            if key in parsed_yaml:
                sections[key] = parsed_yaml[key]
        
        section_count = len(sections)
        logger.info(f"Found {section_count} sections in YAML")
        
        return section_count, sections
        
    except Exception as e:
        logger.error(f"Error counting sections: {str(e)}")
        raise


def convert_numeric_keys_to_strings(data: Any) -> Any:
    """
    Recursively convert numeric dictionary keys to strings for MongoDB compatibility.
    MongoDB requires all dictionary keys to be strings.
    
    Args:
        data: Data structure to convert (dict, list, or primitive)
        
    Returns:
        Any: Converted data structure with string keys
    """
    try:
        if isinstance(data, dict):
            # Convert all keys to strings and recursively process values
            return {str(k): convert_numeric_keys_to_strings(v) for k, v in data.items()}
        elif isinstance(data, list):
            # Recursively process list items
            return [convert_numeric_keys_to_strings(item) for item in data]
        else:
            # Return primitive values as-is
            return data
    except Exception as e:
        logger.error(f"Error converting numeric keys: {str(e)}")
        raise
