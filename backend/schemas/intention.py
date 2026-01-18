"""
Intention schema models for intent interpretation endpoint.
Defines strict structure for LLM-generated intent JSON.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Literal
from enum import Enum
import uuid


class TargetSection(str, Enum):
    """Allowed target sections in Domain Pack YAML."""
    NAME = "name"
    DESCRIPTION = "description"
    VERSION = "version"
    ENTITIES = "entities"
    KEY_TERMS = "key_terms"
    ENTITY_ALIASES = "entity_aliases"
    EXTRACTION_PATTERNS = "extraction_patterns"
    BUSINESS_CONTEXT = "business_context"
    RELATIONSHIP_TYPES = "relationship_types"
    RELATIONSHIPS = "relationships"
    BUSINESS_PATTERNS = "business_patterns"
    REASONING_TEMPLATES = "reasoning_templates"
    MULTIHOP_QUESTIONS = "multihop_questions"
    QUESTION_TEMPLATES = "question_templates"
    BUSINESS_RULES = "business_rules"
    VALIDATION_RULES = "validation_rules"


class Operation(str, Enum):
    """Allowed operations on Domain Pack sections."""
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    REORDER = "REORDER"


class ExecutionRisk(str, Enum):
    """Risk level for executing the intent."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class EntityInvolved(BaseModel):
    """Entity involved in the intent."""
    type: str = Field(..., description="Type of entity (e.g., ENTITY, RELATIONSHIP)")
    name: str = Field(..., description="Name of the entity")


class IntentPayload(BaseModel):
    """Payload containing explicit and implicit data from user request."""
    explicit: Dict[str, Any] = Field(
        default_factory=dict,
        description="Explicitly stated data from user request"
    )
    implicit: Dict[str, Any] = Field(
        default_factory=dict,
        description="Implicit or inferred data"
    )


class IntentConstraints(BaseModel):
    """Constraints on intent execution."""
    must_not_override_existing: bool = Field(
        default=True,
        description="Whether to prevent overriding existing data"
    )
    additional_constraints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional custom constraints"
    )


class ValidationRequirements(BaseModel):
    """Validation requirements for intent execution."""
    schema_validation: bool = Field(
        default=True,
        description="Whether to perform schema validation"
    )
    duplicate_check: bool = Field(
        default=True,
        description="Whether to check for duplicates"
    )
    additional_validations: Dict[str, bool] = Field(
        default_factory=dict,
        description="Additional validation requirements"
    )


class IntentionSchema(BaseModel):
    """
    Main intention schema for structured intent representation.
    
    This schema represents a parsed and structured user intent
    for modifying a Domain Pack YAML file.
    """
    intent_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this intent"
    )
    domain_pack_id: str = Field(..., description="Target domain pack ID")
    target_section: TargetSection = Field(..., description="Target section to modify")
    operation: Operation = Field(..., description="Operation to perform")
    intent_summary: str = Field(..., description="Human-readable summary of intent")
    confidence: float = Field(
        ...,
        description="Confidence score (0.0 to 1.0)",
        ge=0.0,
        le=1.0
    )
    entities_involved: List[EntityInvolved] = Field(
        default_factory=list,
        description="Entities involved in this intent"
    )
    payload: IntentPayload = Field(..., description="Intent payload data")
    constraints: IntentConstraints = Field(
        default_factory=IntentConstraints,
        description="Execution constraints"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Assumptions made during interpretation"
    )
    ambiguities: List[str] = Field(
        default_factory=list,
        description="Detected ambiguities in user request"
    )
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement or clarification"
    )
    validation_requirements: ValidationRequirements = Field(
        default_factory=ValidationRequirements,
        description="Validation requirements"
    )
    execution_risk: ExecutionRisk = Field(..., description="Risk level for execution")
    
    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Validate confidence is between 0.0 and 1.0."""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v


class IntentRequest(BaseModel):
    """Request model for /intent endpoint."""
    domain_pack_id: str = Field(..., description="Domain pack ID to modify")
    domain_name: str = Field(..., description="Domain name")
    description: str = Field(..., description="Domain description")
    user_request: str = Field(..., description="Natural language user request")
    
    @field_validator('user_request')
    @classmethod
    def validate_user_request(cls, v: str) -> str:
        """Validate user request is not empty."""
        if not v or not v.strip():
            raise ValueError('User request cannot be empty')
        return v.strip()


class IntentResponse(BaseModel):
    """Response model for /intent endpoint."""
    intent: IntentionSchema = Field(..., description="Parsed intention schema")
    message: str = Field(
        default="Intent parsed successfully",
        description="Response message"
    )


class IntentErrorResponse(BaseModel):
    """Error response for /intent endpoint (fail-safe)."""
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    confidence: float = Field(default=0.0, description="Confidence (always 0.0 for errors)")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )
