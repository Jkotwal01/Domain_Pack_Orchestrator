"""
Intent interpretation endpoint.
Converts natural language requests to structured IntentionSchema using LLM.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from core.logging_config import logger
from schemas.intention import (
    IntentRequest,
    IntentResponse,
    IntentionSchema,
    IntentErrorResponse
)
from services.llm_service import generate_intent


router = APIRouter()


@router.post("/intent", response_model=IntentResponse, status_code=status.HTTP_200_OK)
async def interpret_intent(request: IntentRequest) -> IntentResponse:
    """
    Convert natural language user request to structured IntentionSchema.
    
    This endpoint uses LLM integration (Groq/OpenAI/Anthropic) to parse natural language
    requests and generate a strict, machine-readable JSON schema for modifying Domain Pack YAML files.
    
    **How It Works:**
    1. Receives your natural language request
    2. Sends it to the configured LLM (Groq by default)
    3. LLM analyzes and structures the request
    4. Returns validated IntentionSchema JSON
    
    **Request Body:**
    - `domain_pack_id`: ID of the domain pack to modify
    - `domain_name`: Name of the domain (e.g., "legal", "healthcare")
    - `description`: Brief description of the domain
    - `user_request`: Natural language request (e.g., "Add new entity CLIENT with attributes client_id, name, type")
    
    **Response Fields:**
    - `target_section`: Which YAML section to modify (entities, relationships, etc.)
    - `operation`: What to do (ADD, UPDATE, DELETE, MERGE, SPLIT, REORDER)
    - `confidence`: How confident the LLM is (0.0 to 1.0)
    - `execution_risk`: Risk level (LOW, MEDIUM, HIGH)
    - `ambiguities`: List of unclear parts in your request
    - `suggestions`: Helpful suggestions from the LLM
    
    **Example Request:**
    ```json
    {
      "domain_pack_id": "Legal_v01",
      "domain_name": "legal",
      "description": "Legal and compliance domain",
      "user_request": "Add new entity CLIENT with attributes client_id, name, type"
    }
    ```
    
    **Error Codes:**
    - `LLM_CONFIGURATION_ERROR`: API key not configured
    - `LLM_API_ERROR`: LLM service failed
    - `INVALID_INTENT_SCHEMA`: LLM output doesn't match schema
    
    **Tips:**
    - Be specific in your request for higher confidence
    - Check `/intent/health` first to verify LLM is configured
    - Low confidence (<0.5) means request needs clarification
    """
    try:
        logger.info(f"Received intent request for domain pack: {request.domain_pack_id}")
        logger.info(f"User request: {request.user_request}")
        
        # Generate intent using LLM
        try:
            intent_data = generate_intent(
                domain_pack_id=request.domain_pack_id,
                domain_name=request.domain_name,
                description=request.description,
                user_request=request.user_request
            )
        except ValueError as e:
            # Configuration error (missing API key, etc.)
            logger.error(f"LLM configuration error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "LLM_CONFIGURATION_ERROR",
                    "message": f"LLM service not properly configured: {str(e)}",
                    "confidence": 0.0
                }
            )
        except Exception as e:
            # LLM API error
            logger.error(f"LLM API error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "LLM_API_ERROR",
                    "message": f"Failed to generate intent: {str(e)}",
                    "confidence": 0.0
                }
            )
        
        # Validate intent data against IntentionSchema
        try:
            intent_schema = IntentionSchema(**intent_data)
            logger.info(f"Intent validated successfully with confidence: {intent_schema.confidence}")
            
            # Log warnings if confidence is low or ambiguities detected
            if intent_schema.confidence < 0.5:
                logger.warning(f"Low confidence intent: {intent_schema.confidence}")
            if intent_schema.ambiguities:
                logger.warning(f"Ambiguities detected: {intent_schema.ambiguities}")
            if intent_schema.execution_risk == "HIGH":
                logger.warning(f"High execution risk detected")
            
            return IntentResponse(
                intent=intent_schema,
                message="Intent parsed successfully"
            )
            
        except ValidationError as e:
            # Pydantic validation failed - LLM output doesn't match schema
            logger.error(f"Intent validation failed: {str(e)}")
            logger.error(f"Invalid intent data: {intent_data}")
            
            # Return fail-safe response
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": "INVALID_INTENT_SCHEMA",
                    "message": "The intent could not be parsed safely. LLM output does not match required schema.",
                    "confidence": 0.0,
                    "details": {
                        "validation_errors": str(e),
                        "llm_output": intent_data
                    }
                }
            )
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in intent endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": f"An unexpected error occurred: {str(e)}",
                "confidence": 0.0
            }
        )


@router.get("/intent/health", status_code=status.HTTP_200_OK)
async def intent_health_check():
    """
    Health check for intent interpretation service.
    
    Verifies LLM provider configuration without making an API call.
    This is a fast, free diagnostic tool to check if the LLM service is ready.
    
    **Status Meanings:**
    
    | Status | Condition | What It Means |
    |--------|-----------|---------------|
    | `healthy` | API key is configured | ✅ Everything working, ready to use |
    | `degraded` | No API key but config is valid | ⚠️ Config loads fine, just missing API key |
    | `unhealthy` | Exception during health check | ❌ Serious configuration problem |
    
    **Returns:**
    - `status`: Health status (healthy/degraded/unhealthy)
    - `llm_provider`: Which LLM provider is configured (openai/groq/anthropic)
    - `llm_model`: Which model will be used
    - `api_key_configured`: Whether the API key is set
    - `message`: Human-readable status message
    
    **Example Response (Healthy):**
    ```json
    {
      "status": "healthy",
      "llm_provider": "groq",
      "llm_model": "llama-3.3-70b-versatile",
      "api_key_configured": true,
      "message": "LLM service configured"
    }
    ```
    
    **Use Cases:**
    - Pre-deployment verification
    - Troubleshooting intent endpoint failures
    - Monitoring LLM service availability
    """
    try:
        from core.config import settings
        
        # Check if API key is configured for selected provider
        provider = settings.LLM_PROVIDER.lower()
        api_key_configured = False
        
        if provider == "openai" and settings.OPENAI_API_KEY:
            api_key_configured = True
        elif provider == "groq" and settings.GROQ_API_KEY:
            api_key_configured = True
        elif provider == "anthropic" and settings.ANTHROPIC_API_KEY:
            api_key_configured = True
        
        status_msg = "healthy" if api_key_configured else "degraded"
        
        return {
            "status": status_msg,
            "llm_provider": provider,
            "llm_model": settings.LLM_MODEL,
            "api_key_configured": api_key_configured,
            "message": "LLM service configured" if api_key_configured else "LLM API key not configured"
        }
        
    except Exception as e:
        logger.error(f"Intent health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"Configuration error: {str(e)}"
        }
