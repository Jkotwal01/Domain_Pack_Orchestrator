"""
Question template Pydantic models.
Validates question_templates and multihop_questions sections.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class QuestionTemplateModel(BaseModel):
    """
    Model for individual question template.
    
    Attributes:
        template: Question template string (required)
        entity_types: List of applicable entity types (optional)
        entity_pairs: List of entity pairs for relationship questions (optional)
        process_types: List of process types (optional)
        financial_types: List of financial types (optional)
        attributes: List of attributes (optional)
        priority: Question priority level (required)
        expected_answer_type: Expected answer type (required)
    """
    template: str = Field(..., description="Question template string")
    entity_types: Optional[List[str]] = Field(default=None, description="Applicable entity types")
    entity_pairs: Optional[List[List[str]]] = Field(default=None, description="Entity pairs for relationships")
    process_types: Optional[List[str]] = Field(default=None, description="Process types")
    financial_types: Optional[List[str]] = Field(default=None, description="Financial types")
    attributes: Optional[List[str]] = Field(default=None, description="Attributes")
    priority: str = Field(..., description="Question priority level")
    expected_answer_type: str = Field(..., description="Expected answer type")


class QuestionTemplatesModel(BaseModel):
    """
    Model for question templates collection.
    Groups templates by category.
    
    Attributes:
        entity_extraction: Entity extraction questions (optional)
        relationship_extraction: Relationship extraction questions (optional)
        business_process: Business process questions (optional)
        financial_extraction: Financial extraction questions (optional)
    """
    entity_extraction: Optional[List[QuestionTemplateModel]] = Field(
        default=None, 
        description="Entity extraction questions"
    )
    relationship_extraction: Optional[List[QuestionTemplateModel]] = Field(
        default=None, 
        description="Relationship extraction questions"
    )
    business_process: Optional[List[QuestionTemplateModel]] = Field(
        default=None, 
        description="Business process questions"
    )
    financial_extraction: Optional[List[QuestionTemplateModel]] = Field(
        default=None, 
        description="Financial extraction questions"
    )
    
    class Config:
        """Pydantic configuration"""
        extra = "allow"  # Allow additional question categories


class MultihopQuestionModel(BaseModel):
    """
    Model for multihop question definition.
    
    Attributes:
        template: Question template (required)
        examples: List of example questions (optional)
        priority: Question priority (required)
        reasoning_type: Type of reasoning required (required)
    """
    template: str = Field(..., description="Question template")
    examples: Optional[List[str]] = Field(default=None, description="Example questions")
    priority: str = Field(..., description="Question priority")
    reasoning_type: str = Field(..., description="Type of reasoning required")
