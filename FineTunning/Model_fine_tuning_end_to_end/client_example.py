"""
API Client Example
Shows how to use the deployed API in your applications
"""

import requests
import json

class LLMClient:
    """Client for interacting with LLM API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def check_health(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def list_models(self):
        """List available models"""
        response = requests.get(f"{self.base_url}/api/models")
        return response.json()
    
    def query_hr(self, question, max_tokens=200, temperature=0.7):
        """Query HR model"""
        return self._query("hr", question, max_tokens, temperature)
    
    def query_finance(self, question, max_tokens=200, temperature=0.7):
        """Query Finance model"""
        return self._query("finance", question, max_tokens, temperature)
    
    def query_sales(self, question, max_tokens=200, temperature=0.7):
        """Query Sales model"""
        return self._query("sales", question, max_tokens, temperature)
    
    def query_healthcare(self, question, max_tokens=200, temperature=0.7):
        """Query Healthcare model"""
        return self._query("healthcare", question, max_tokens, temperature)
    
    def query_marketing(self, question, max_tokens=200, temperature=0.7):
        """Query Marketing model"""
        return self._query("marketing", question, max_tokens, temperature)
    
    def query_any(self, model, question, max_tokens=200, temperature=0.7):
        """Query any model using generic endpoint"""
        response = requests.post(
            f"{self.base_url}/api/infer/{model}",
            json={
                "query": question,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9
            }
        )
        response.raise_for_status()
        return response.json()
    
    def _query(self, model, question, max_tokens, temperature):
        """Internal query method"""
        response = requests.post(
            f"{self.base_url}/api/{model}",
            json={
                "query": question,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9
            }
        )
        response.raise_for_status()
        return response.json()

# Example usage
if __name__ == "__main__":
    # Initialize client
    client = LLMClient("http://localhost:8000")
    
    print("="*60)
    print("LLM API Client Examples")
    print("="*60)
    
    # Example 1: Check health
    print("\n1. Checking API health...")
    health = client.check_health()
    print(f"   Status: {health['status']}")
    print(f"   GPU: {health['gpu_name']}")
    
    # Example 2: List models
    print("\n2. Listing available models...")
    models = client.list_models()
    print(f"   Found {len(models['models'])} models")
    
    # Example 3: HR Query
    print("\n3. Querying HR model...")
    response = client.query_hr(
        "How do I apply for casual leave?",
        max_tokens=150
    )
    print(f"   Query: {response['query']}")
    print(f"   Response: {response['response'][:100]}...")
    
    # Example 4: Healthcare Query
    print("\n4. Querying Healthcare model...")
    response = client.query_healthcare(
        "What are symptoms of dengue?",
        max_tokens=150
    )
    print(f"   Query: {response['query']}")
    print(f"   Response: {response['response'][:100]}...")
    
    # Example 5: Using generic endpoint
    print("\n5. Using generic endpoint...")
    response = client.query_any(
        "marketing",
        "Create social media strategy",
        max_tokens=150
    )
    print(f"   Model: {response['model']}")
    print(f"   Response: {response['response'][:100]}...")
    
    print("\n" + "="*60)
    print("✓ All examples completed!")
    print("="*60)

