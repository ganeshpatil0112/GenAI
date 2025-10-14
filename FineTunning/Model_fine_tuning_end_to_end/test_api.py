"""
API Testing Client
Test your deployed API endpoints
"""

import requests
import json
import time

# API base URL (change this to your deployed URL)
API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_list_models():
    """List all available models"""
    print("\n" + "="*60)
    print("Listing Available Models")
    print("="*60)
    
    response = requests.get(f"{API_URL}/api/models")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_inference(model: str, query: str, max_tokens: int = 200):
    """Test inference endpoint"""
    print("\n" + "="*60)
    print(f"Testing {model.upper()} Model")
    print("="*60)
    print(f"Query: {query}")
    print("\nGenerating response...")
    
    start_time = time.time()
    
    response = requests.post(
        f"{API_URL}/api/{model}",
        json={
            "query": query,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    
    elapsed = time.time() - start_time
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse:")
        print("-" * 60)
        print(data['response'])
        print("-" * 60)
        print(f"\nTokens Generated: {data['tokens_generated']}")
        print(f"Time Taken: {elapsed:.2f}s")
    else:
        print(f"Error: {response.text}")

def test_generic_endpoint(model: str, query: str):
    """Test generic inference endpoint"""
    print("\n" + "="*60)
    print(f"Testing Generic Endpoint with {model.upper()}")
    print("="*60)
    
    response = requests.post(
        f"{API_URL}/api/infer/{model}",
        json={
            "query": query,
            "max_tokens": 150
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:200]}...")
    else:
        print(f"Error: {response.text}")

def run_all_tests():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print(" "*20 + "API TEST SUITE")
    print("="*70)
    
    # Test 1: Health check
    try:
        test_health()
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test 2: List models
    try:
        test_list_models()
    except Exception as e:
        print(f"⚠️  List models failed: {e}")
    
    # Test 3: HR Model
    try:
        test_inference(
            "hr",
            "How do I apply for casual leave in the company?"
        )
    except Exception as e:
        print(f"⚠️  HR model test failed: {e}")
    
    # Test 4: Sales Model
    try:
        test_inference(
            "sales",
            "Customer wants to return a product bought during sale"
        )
    except Exception as e:
        print(f"⚠️  Sales model test failed: {e}")
    
    # Test 5: Healthcare Model
    try:
        test_inference(
            "healthcare",
            "What are the symptoms of dengue fever?"
        )
    except Exception as e:
        print(f"⚠️  Healthcare model test failed: {e}")
    
    # Test 6: Marketing Model
    try:
        test_inference(
            "marketing",
            "Create a Diwali marketing campaign for e-commerce platform"
        )
    except Exception as e:
        print(f"⚠️  Marketing model test failed: {e}")
    
    # Test 7: Generic endpoint
    try:
        test_generic_endpoint("healthcare", "How to prevent malaria?")
    except Exception as e:
        print(f"⚠️  Generic endpoint test failed: {e}")
    
    print("\n" + "="*70)
    print("✓ Test Suite Completed!")
    print("="*70 + "\n")

if __name__ == "__main__":
    print("\nAPI Testing Client")
    print("Make sure the API server is running at", API_URL)
    print("\nStarting tests in 2 seconds...")
    time.sleep(2)
    
    run_all_tests()

