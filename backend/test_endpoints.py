"""
Test script for FastAPI endpoints.
Tests /upload and /validate endpoints with sample YAML file.
"""

import requests
import json

BASE_URL = "http://localhost:8000"
SAMPLE_YAML_PATH = "d:/Anti/sample.yaml"

def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_validate_endpoint():
    """Test /validate endpoint with sample YAML"""
    print("\n" + "="*60)
    print("Testing /validate Endpoint")
    print("="*60)
    
    try:
        with open(SAMPLE_YAML_PATH, 'rb') as f:
            files = {'file': ('sample.yaml', f, 'application/x-yaml')}
            response = requests.post(f"{BASE_URL}/validate", files=files)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"\nValidation Result:")
        print(f"  is_valid: {result.get('is_valid')}")
        print(f"  errors: {len(result.get('errors', []))} errors")
        print(f"  warnings: {len(result.get('warnings', []))} warnings")
        
        if result.get('errors'):
            print(f"\nErrors:")
            for i, error in enumerate(result['errors'][:5], 1):  # Show first 5
                print(f"  {i}. {error}")
        
        if result.get('warnings'):
            print(f"\nWarnings:")
            for i, warning in enumerate(result['warnings'][:5], 1):
                print(f"  {i}. {warning}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_upload_endpoint():
    """Test /upload endpoint with sample YAML"""
    print("\n" + "="*60)
    print("Testing /upload Endpoint")
    print("="*60)
    
    try:
        with open(SAMPLE_YAML_PATH, 'rb') as f:
            files = {'file': ('sample.yaml', f, 'application/x-yaml')}
            response = requests.post(f"{BASE_URL}/upload", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"\nUpload Result:")
            print(f"  document_id: {result.get('document_id')}")
            print(f"  filename: {result.get('filename')}")
            print(f"  sections_count: {result.get('sections_count')}")
            print(f"  metadata:")
            metadata = result.get('metadata', {})
            print(f"    name: {metadata.get('name')}")
            print(f"    description: {metadata.get('description')}")
            print(f"    version: {metadata.get('version')}")
            print(f"\n✓ {result.get('message')}")
            return True
        else:
            print(f"✗ Upload failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_domain_pack_list_endpoint():
    """Test /domain_pack_list endpoint"""
    print("\n" + "="*60)
    print("Testing /domain_pack_list Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/domain_pack_list")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nDomain Pack List Result:")
            print(f"  total_count: {result.get('total_count')}")
            print(f"  domain_packs: {len(result.get('domain_packs', []))} items")
            
            # Display first 3 items
            domain_packs = result.get('domain_packs', [])
            if domain_packs:
                print(f"\n  First {min(3, len(domain_packs))} items:")
                for i, pack in enumerate(domain_packs[:3], 1):
                    print(f"    {i}. {pack.get('domain_name')} (ID: {pack.get('domain_pack_id')[:8]}...)")
                    print(f"       Description: {pack.get('description')}")
                    print(f"       Uploaded: {pack.get('uploaded_at')}")
                
                # Verify sorting (most recent first)
                if len(domain_packs) > 1:
                    from datetime import datetime
                    dates = [datetime.fromisoformat(p['uploaded_at']) for p in domain_packs]
                    is_sorted = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
                    if is_sorted:
                        print(f"\n  ✓ Items are correctly sorted by upload time (most recent first)")
                    else:
                        print(f"\n  ✗ WARNING: Items are NOT sorted correctly")
            else:
                print(f"\n  No domain packs found in database")
            
            print(f"\n✓ Domain pack list retrieved successfully")
            return True
        else:
            print(f"✗ Request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FastAPI Backend Test Suite")
    print("="*60)
    
    results = {
        "Health Check": test_health_check(),
        "Validate Endpoint": test_validate_endpoint(),
        "Upload Endpoint": test_upload_endpoint(),
        "Domain Pack List": test_domain_pack_list_endpoint()
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
