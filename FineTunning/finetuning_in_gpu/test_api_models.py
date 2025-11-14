#!/usr/bin/env python3
"""
Test script to verify API endpoints with available models
"""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")

def test_models():
    """Test models list endpoint"""
    try:
        response = requests.get(f"{API_URL}/api/models")
        print(f"✅ Models list: {response.status_code}")
        print(f"   Available models: {response.json()}")
    except Exception as e:
        print(f"❌ Models list failed: {e}")

def test_model_inference(model_name, query):
    """Test specific model inference"""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "query": query,
            "max_tokens": 100,
            "temperature": 0.7
        }
        response = requests.post(
            f"{API_URL}/api/{model_name}", 
            headers=headers, 
            data=json.dumps(payload)
        )
        print(f"✅ {model_name.upper()} model: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Query: {result['query']}")
            print(f"   Response: {result['response'][:100]}...")
            print(f"   Tokens: {result['tokens_generated']}")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ {model_name.upper()} model failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing API with H100 Models")
    print("=" * 50)
    
    # Test health
    test_health()
    print()
    
    # Test models list
    test_models()
    print()
    
    # Test each model
    models_to_test = [
        ("hr", "What is the company leave policy?"),
        ("finance", "What is the current GST rate?"),
        ("sales", "How can I improve customer satisfaction?"),
        ("healthcare", "What are the benefits of yoga?"),
        ("marketing", "How to create an effective social media campaign?")
    ]
    
    for model_name, query in models_to_test:
        test_model_inference(model_name, query)
        print()
    
    print("🎉 API testing completed!")
