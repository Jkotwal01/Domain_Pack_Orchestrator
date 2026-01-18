"""
LLM service for intent interpretation.
Supports multiple LLM providers (OpenAI, Groq, Anthropic).
"""

import json
import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from tenacity import retry, stop_after_attempt, wait_exponential
from core.config import settings
from core.logging_config import logger


# System prompt template (LLM-agnostic)
SYSTEM_PROMPT = """You are an Intent Interpretation Engine for a Domain Pack Management System.

Your task:
Convert a natural language user request into a STRICT, MACHINE-READABLE JSON object called IntentionSchema.

This system manages structured YAML Domain Packs with EXACTLY the following top-level sections:
- name
- description
- version
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

RULES YOU MUST FOLLOW:
1. You MUST output VALID JSON only.
2. You MUST NOT include explanations, markdown, or commentary.
3. You MUST choose EXACTLY ONE target_section.
4. You MUST choose EXACTLY ONE operation from:
   ADD, UPDATE, DELETE, MERGE, SPLIT, REORDER
5. You MUST include ambiguity detection if any part of the request is underspecified.
6. You MUST NOT invent information that the user did not provide.
7. You MAY suggest reasonable domain-relevant enhancements in the "suggestions" field.
8. You MUST assess execution risk conservatively.
9. Confidence MUST be between 0.0 and 1.0.

If the user request is unclear, ambiguous, or unsafe:
- Populate the "ambiguities" field
- Reduce confidence
- DO NOT assume missing details

REQUIRED OUTPUT FORMAT (STRICT):
{
  "intent_id": "string",
  "domain_pack_id": "string",
  "target_section": "string",
  "operation": "string",
  "intent_summary": "string",
  "confidence": 0.9,
  "entities_involved": [
    {
      "type": "ENTITY",
      "name": "EntityName"
    }
  ],
  "payload": {
    "explicit": {
      "key": "value"
    },
    "implicit": {
      "key": "value"
    }
  },
  "constraints": {
    "must_not_override_existing": true,
    "additional_constraints": {}
  },
  "assumptions": ["assumption1", "assumption2"],
  "ambiguities": ["ambiguity1"],
  "suggestions": ["suggestion1"],
  "validation_requirements": {
    "schema_validation": true,
    "duplicate_check": true,
    "additional_validations": {}
  },
  "execution_risk": "LOW"
}

CRITICAL SCHEMA RULES:
- entities_involved MUST be array of objects with "type" and "name" fields, NOT strings
- payload MUST have "explicit" and "implicit" objects
- constraints MUST have "must_not_override_existing" boolean and "additional_constraints" object
- validation_requirements MUST have "schema_validation", "duplicate_check" booleans and "additional_validations" object
- execution_risk MUST be exactly "LOW", "MEDIUM", or "HIGH"
"""


def create_user_message(domain_pack_id: str, domain_name: str, description: str, user_request: str) -> str:
    """Create user message with injected variables."""
    return f"""Domain Pack ID: {domain_pack_id}
Domain Name: {domain_name}
Domain Description: {description}

User Request:
{user_request}"""


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, system_prompt: str, user_message: str) -> str:
        """Generate response from LLM."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""
    
    def __init__(self):
        try:
            from openai import OpenAI
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not configured")
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("OpenAI provider initialized")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self, system_prompt: str, user_message: str) -> str:
        """Generate response using OpenAI API."""
        try:
            logger.info(f"Calling OpenAI API with model: {settings.LLM_MODEL}")
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                timeout=settings.LLM_TIMEOUT
            )
            content = response.choices[0].message.content
            logger.info("OpenAI API call successful")
            return content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


class GroqProvider(LLMProvider):
    """Groq provider implementation."""
    
    def __init__(self):
        try:
            from groq import Groq
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not configured")
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("Groq provider initialized")
        except ImportError:
            raise ImportError("groq package not installed. Run: pip install groq")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self, system_prompt: str, user_message: str) -> str:
        """Generate response using Groq API."""
        try:
            logger.info(f"Calling Groq API with model: {settings.LLM_MODEL}")
            response = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                timeout=settings.LLM_TIMEOUT
            )
            content = response.choices[0].message.content
            logger.info("Groq API call successful")
            return content
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            raise


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation."""
    
    def __init__(self):
        try:
            from anthropic import Anthropic
            if not settings.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            logger.info("Anthropic provider initialized")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(self, system_prompt: str, user_message: str) -> str:
        """Generate response using Anthropic API."""
        try:
            logger.info(f"Calling Anthropic API with model: {settings.LLM_MODEL}")
            response = self.client.messages.create(
                model=settings.LLM_MODEL,
                max_tokens=settings.LLM_MAX_TOKENS,
                temperature=settings.LLM_TEMPERATURE,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                timeout=settings.LLM_TIMEOUT
            )
            content = response.content[0].text
            logger.info("Anthropic API call successful")
            return content
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise


def get_llm_provider() -> LLMProvider:
    """Get LLM provider based on configuration."""
    provider_name = settings.LLM_PROVIDER.lower()
    
    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "groq":
        return GroqProvider()
    elif provider_name == "anthropic":
        return AnthropicProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")


def parse_llm_output(raw_output: str) -> Dict[str, Any]:
    """
    Parse LLM output to extract JSON.
    
    Handles cases where LLM might include markdown code blocks or extra text.
    """
    try:
        # Try direct JSON parse first
        return json.loads(raw_output)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        if "```json" in raw_output:
            start = raw_output.find("```json") + 7
            end = raw_output.find("```", start)
            json_str = raw_output[start:end].strip()
            return json.loads(json_str)
        elif "```" in raw_output:
            start = raw_output.find("```") + 3
            end = raw_output.find("```", start)
            json_str = raw_output[start:end].strip()
            return json.loads(json_str)
        else:
            # Try to find JSON object in the text
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            if start != -1 and end > start:
                json_str = raw_output[start:end]
                return json.loads(json_str)
            raise ValueError("Could not extract valid JSON from LLM output")


def normalize_intent_data(intent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize LLM output to match IntentionSchema structure.
    
    Fixes common schema mismatches:
    - Converts entities_involved strings to objects
    - Ensures payload has explicit/implicit structure
    - Adds missing required fields with defaults
    """
    normalized = intent_data.copy()
    
    # Fix entities_involved: convert strings to objects
    if "entities_involved" in normalized:
        entities = normalized["entities_involved"]
        if isinstance(entities, list):
            fixed_entities = []
            for entity in entities:
                if isinstance(entity, str):
                    # Convert string to object
                    fixed_entities.append({
                        "type": "ENTITY",
                        "name": entity
                    })
                elif isinstance(entity, dict):
                    # Ensure it has type and name
                    if "name" in entity and "type" not in entity:
                        entity["type"] = "ENTITY"
                    fixed_entities.append(entity)
            normalized["entities_involved"] = fixed_entities
    
    # Fix payload: ensure explicit/implicit structure
    if "payload" in normalized:
        payload = normalized["payload"]
        if isinstance(payload, dict):
            # If payload doesn't have explicit/implicit structure, wrap it
            if "explicit" not in payload and "implicit" not in payload:
                normalized["payload"] = {
                    "explicit": payload,
                    "implicit": {}
                }
            else:
                # Ensure both keys exist
                if "explicit" not in payload:
                    payload["explicit"] = {}
                if "implicit" not in payload:
                    payload["implicit"] = {}
    else:
        normalized["payload"] = {"explicit": {}, "implicit": {}}
    
    # Fix constraints: ensure proper structure
    if "constraints" in normalized:
        constraints = normalized["constraints"]
        if isinstance(constraints, dict):
            # Ensure must_not_override_existing exists
            if "must_not_override_existing" not in constraints:
                constraints["must_not_override_existing"] = True
            # Ensure additional_constraints exists
            if "additional_constraints" not in constraints:
                constraints["additional_constraints"] = {}
    else:
        normalized["constraints"] = {
            "must_not_override_existing": True,
            "additional_constraints": {}
        }
    
    # Fix validation_requirements: ensure proper structure
    if "validation_requirements" in normalized:
        val_reqs = normalized["validation_requirements"]
        if isinstance(val_reqs, dict):
            # Ensure required boolean fields exist
            if "schema_validation" not in val_reqs:
                val_reqs["schema_validation"] = True
            if "duplicate_check" not in val_reqs:
                val_reqs["duplicate_check"] = True
            # Ensure additional_validations exists
            if "additional_validations" not in val_reqs:
                val_reqs["additional_validations"] = {}
    else:
        normalized["validation_requirements"] = {
            "schema_validation": True,
            "duplicate_check": True,
            "additional_validations": {}
        }
    
    # Ensure default values for optional fields
    if "assumptions" not in normalized:
        normalized["assumptions"] = []
    if "ambiguities" not in normalized:
        normalized["ambiguities"] = []
    if "suggestions" not in normalized:
        normalized["suggestions"] = []
    
    return normalized


def generate_intent(
    domain_pack_id: str,
    domain_name: str,
    description: str,
    user_request: str
) -> Dict[str, Any]:
    """
    Generate intent schema from user request using LLM.
    
    Args:
        domain_pack_id: Domain pack ID
        domain_name: Domain name
        description: Domain description
        user_request: Natural language user request
        
    Returns:
        Dict containing parsed intent schema
        
    Raises:
        Exception: If LLM call fails or output cannot be parsed
    """
    try:
        logger.info(f"Generating intent for domain pack: {domain_pack_id}")
        logger.info(f"User request: {user_request}")
        
        # Get LLM provider
        provider = get_llm_provider()
        
        # Create user message
        user_message = create_user_message(domain_pack_id, domain_name, description, user_request)
        
        # Generate response
        start_time = time.time()
        raw_output = provider.generate(SYSTEM_PROMPT, user_message)
        elapsed_time = time.time() - start_time
        
        logger.info(f"LLM response received in {elapsed_time:.2f}s")
        logger.debug(f"Raw LLM output: {raw_output}")
        
        # Parse JSON from output
        intent_data = parse_llm_output(raw_output)
        
        # Normalize the data to match schema
        intent_data = normalize_intent_data(intent_data)
        
        # Ensure intent_id and domain_pack_id are set
        if "intent_id" not in intent_data:
            import uuid
            intent_data["intent_id"] = str(uuid.uuid4())
        if "domain_pack_id" not in intent_data:
            intent_data["domain_pack_id"] = domain_pack_id
        
        logger.info(f"Intent generated successfully with confidence: {intent_data.get('confidence', 0.0)}")
        return intent_data
        
    except Exception as e:
        logger.error(f"Error generating intent: {str(e)}", exc_info=True)
        raise
