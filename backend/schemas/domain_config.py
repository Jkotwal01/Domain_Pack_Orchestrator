"""
Root domain config Pydantic model.
Validates the complete YAML structure.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from schemas.entities import EntityModel
from schemas.extraction import ExtractionPatternModel
from schemas.relationships import RelationshipModel, RelationshipTypeModel
from schemas.business import BusinessContextModel, BusinessPatternModel, BusinessRuleModel
from schemas.questions import QuestionTemplatesModel, MultihopQuestionModel
from schemas.reasoning import ReasoningTemplateModel


class ValidationRulesModel(BaseModel):
    """
    Model for validation rules section.
    
    Attributes:
        required_fields: Dict mapping entity types to required field lists
    """
    required_fields: Optional[Dict[str, List[str]]] = Field(
        default=None, 
        description="Required fields per entity type"
    )
    
    class Config:
        """Pydantic configuration"""
        extra = "allow"  # Allow additional validation rules


class DomainConfigModel(BaseModel):
    """
    Root model for complete domain config YAML validation.
    
    Required fields:
        - name
        - description
        - version
    
    Optional sections (all can be empty or omitted):
        - entities
        - key_terms
        - entity_aliases
        - extraction_patterns
        - business_context
        - relationship_types
        - relationships
        - business_patterns
        - reasoning_templates
        - multihop_questions
        - question_templates
        - business_rules
        - validation_rules
    """
    
    # Required metadata fields
    name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    version: str = Field(..., description="Domain version")
    
    # Optional sections
    entities: Optional[List[EntityModel]] = Field(
        default=None, 
        description="List of entity definitions"
    )
    
    key_terms: Optional[List[str]] = Field(
        default=None, 
        description="List of key domain terms"
    )
    
    entity_aliases: Optional[Dict[str, List[str]]] = Field(
        default=None, 
        description="Entity type to aliases mapping"
    )
    
    extraction_patterns: Optional[List[ExtractionPatternModel]] = Field(
        default=None, 
        description="List of extraction patterns"
    )
    
    business_context: Optional[BusinessContextModel] = Field(
        default=None, 
        description="Business context configuration"
    )
    
    relationship_types: Optional[List[RelationshipTypeModel]] = Field(
        default=None, 
        description="List of relationship type definitions"
    )
    
    relationships: Optional[List[RelationshipModel]] = Field(
        default=None, 
        description="List of relationship definitions"
    )
    
    business_patterns: Optional[List[BusinessPatternModel]] = Field(
        default=None, 
        description="List of business pattern definitions"
    )
    
    reasoning_templates: Optional[List[ReasoningTemplateModel]] = Field(
        default=None, 
        description="List of reasoning template definitions"
    )
    
    multihop_questions: Optional[List[MultihopQuestionModel]] = Field(
        default=None, 
        description="List of multihop question definitions"
    )
    
    question_templates: Optional[QuestionTemplatesModel] = Field(
        default=None, 
        description="Question templates by category"
    )
    
    business_rules: Optional[List[BusinessRuleModel]] = Field(
        default=None, 
        description="List of business rule definitions"
    )
    
    validation_rules: Optional[ValidationRulesModel] = Field(
        default=None, 
        description="Validation rules configuration"
    )
    
    class Config:
        """Pydantic configuration"""
        # Allow extra fields for future extensibility
        extra = "allow"
        # Use field aliases for better compatibility
        populate_by_name = True
