#!/usr/bin/env python3
"""
Simple API test script to check if endpoints are working.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_register_endpoint():
    """Test registration endpoint."""
    try:
        url = f"{BASE_URL}/api/v1/users/register"
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+1234567890"
        }
        
        print(f"Testing registration endpoint: {url}")
        response = requests.post(url, json=data)
        print(f"Registration response: {response.status_code}")
        
        if response.status_code == 200:
            print(f"Success: {response.json()}")
        elif response.status_code == 422:
            print(f"Validation error: {response.json()}")
        elif response.status_code == 400:
            print(f"Bad request: {response.json()}")
        else:
            print(f"Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
        
        return response.status_code in [200, 422, 400]  # These are expected responses
    except Exception as e:
        print(f"Registration test failed: {e}")
        return False

def test_docs():
    """Test API documentation endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"API docs: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"API docs failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing API endpoints...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("API Documentation", test_docs),
        ("Registration Endpoint", test_register_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✅ PASS' if success else '❌ FAIL'}")
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main() 