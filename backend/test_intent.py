"""
Test script for /intent endpoint.
Tests intent interpretation with various scenarios.
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_intent_health_check():
    """Test intent health check endpoint"""
    print("\n" + "="*60)
    print("Testing Intent Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/intent/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nHealth Check Result:")
            print(f"  status: {result.get('status')}")
            print(f"  llm_provider: {result.get('llm_provider')}")
            print(f"  llm_model: {result.get('llm_model')}")
            print(f"  api_key_configured: {result.get('api_key_configured')}")
            print(f"  message: {result.get('message')}")
            
            if result.get('api_key_configured'):
                print(f"\n✓ LLM service is healthy and configured")
                return True
            else:
                print(f"\n⚠ LLM service is degraded - API key not configured")
                return False
        else:
            print(f"✗ Health check failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_intent_simple_add():
    """Test intent endpoint with simple ADD operation"""
    print("\n" + "="*60)
    print("Testing Intent Endpoint - Simple ADD")
    print("="*60)
    
    try:
        request_data = {
            "domain_pack_id": "Legal_v01",
            "domain_name": "legal",
            "description": "Legal and compliance domain",
            "user_request": "Add new entity CLIENT with attributes client_id, name, type, industry, contact_info"
        }
        
        print(f"\nRequest:")
        print(f"  User Request: {request_data['user_request']}")
        
        response = requests.post(
            f"{BASE_URL}/intent",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent', {})
            
            print(f"\nIntent Result:")
            print(f"  intent_id: {intent.get('intent_id')}")
            print(f"  target_section: {intent.get('target_section')}")
            print(f"  operation: {intent.get('operation')}")
            print(f"  intent_summary: {intent.get('intent_summary')}")
            print(f"  confidence: {intent.get('confidence')}")
            print(f"  execution_risk: {intent.get('execution_risk')}")
            
            if intent.get('entities_involved'):
                print(f"\n  Entities Involved:")
                for entity in intent['entities_involved']:
                    print(f"    - {entity.get('type')}: {entity.get('name')}")
            
            if intent.get('payload'):
                print(f"\n  Payload:")
                print(f"    Explicit: {json.dumps(intent['payload'].get('explicit', {}), indent=6)}")
                if intent['payload'].get('implicit'):
                    print(f"    Implicit: {json.dumps(intent['payload'].get('implicit', {}), indent=6)}")
            
            if intent.get('ambiguities'):
                print(f"\n  Ambiguities:")
                for amb in intent['ambiguities']:
                    print(f"    - {amb}")
            
            if intent.get('suggestions'):
                print(f"\n  Suggestions:")
                for sug in intent['suggestions']:
                    print(f"    - {sug}")
            
            print(f"\n✓ Intent parsed successfully")
            return True
        else:
            print(f"✗ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_intent_ambiguous_request():
    """Test intent endpoint with ambiguous request"""
    print("\n" + "="*60)
    print("Testing Intent Endpoint - Ambiguous Request")
    print("="*60)
    
    try:
        request_data = {
            "domain_pack_id": "Legal_v01",
            "domain_name": "legal",
            "description": "Legal and compliance domain",
            "user_request": "Update the entity with new attributes"
        }
        
        print(f"\nRequest:")
        print(f"  User Request: {request_data['user_request']}")
        
        response = requests.post(
            f"{BASE_URL}/intent",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent', {})
            
            print(f"\nIntent Result:")
            print(f"  confidence: {intent.get('confidence')}")
            print(f"  execution_risk: {intent.get('execution_risk')}")
            
            if intent.get('ambiguities'):
                print(f"\n  Ambiguities Detected:")
                for amb in intent['ambiguities']:
                    print(f"    - {amb}")
                print(f"\n✓ Ambiguities correctly detected")
            else:
                print(f"\n⚠ No ambiguities detected (expected some)")
            
            return True
        else:
            print(f"✗ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_intent_complex_request():
    """Test intent endpoint with complex multi-attribute request"""
    print("\n" + "="*60)
    print("Testing Intent Endpoint - Complex Request")
    print("="*60)
    
    try:
        request_data = {
            "domain_pack_id": "Legal_v01",
            "domain_name": "legal",
            "description": "Legal and compliance domain",
            "user_request": "Add new entity CLIENT with attributes client_id, name, type, industry, contact_info and 4 more attributes related to CLIENT entity"
        }
        
        print(f"\nRequest:")
        print(f"  User Request: {request_data['user_request']}")
        
        response = requests.post(
            f"{BASE_URL}/intent",
            json=request_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            intent = result.get('intent', {})
            
            print(f"\nIntent Result:")
            print(f"  target_section: {intent.get('target_section')}")
            print(f"  operation: {intent.get('operation')}")
            print(f"  confidence: {intent.get('confidence')}")
            
            if intent.get('suggestions'):
                print(f"\n  Suggestions for additional attributes:")
                for sug in intent['suggestions']:
                    print(f"    - {sug}")
            
            print(f"\n✓ Complex request handled successfully")
            return True
        else:
            print(f"✗ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    """Run all intent tests"""
    print("\n" + "="*60)
    print("Intent Endpoint Test Suite")
    print("="*60)
    
    results = {
        "Intent Health Check": test_intent_health_check(),
        "Simple ADD Intent": test_intent_simple_add(),
        "Ambiguous Request": test_intent_ambiguous_request(),
        "Complex Request": test_intent_complex_request()
    }
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    
    return all_passed


if __name__ == "__main__":
    main()
