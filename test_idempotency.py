#!/usr/bin/env python3
"""
Simple test to verify idempotency behavior.
Run this after starting the backend server.
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_idempotency():
    """Test that duplicate requests with same idempotency key return same result"""
    
    # Test data
    test_expense = {
        "idempotency_key": f"test-{int(time.time())}",
        "amount": 25.50,
        "category": "Test",
        "description": "Idempotency test",
        "date": "2024-01-15"
    }
    
    print("Testing idempotency...")
    print(f"Using idempotency key: {test_expense['idempotency_key']}")
    
    # First request
    print("\n1. Making first request...")
    response1 = requests.post(f"{API_BASE}/expenses", json=test_expense)
    
    if response1.status_code != 200:
        print(f"First request failed: {response1.status_code}")
        print(response1.text)
        return False
    
    expense1 = response1.json()
    print(f"Created expense with ID: {expense1['id']}")
    
    # Second request with same idempotency key but different data
    test_expense_duplicate = test_expense.copy()
    test_expense_duplicate["amount"] = 99.99  # Different amount
    test_expense_duplicate["description"] = "Should be ignored"  # Different description
    
    print("\n2. Making duplicate request with different data...")
    response2 = requests.post(f"{API_BASE}/expenses", json=test_expense_duplicate)
    
    if response2.status_code != 200:
        print(f"Second request failed: {response2.status_code}")
        print(response2.text)
        return False
    
    expense2 = response2.json()
    print(f"Returned expense with ID: {expense2['id']}")
    
    # Verify they are the same
    if expense1['id'] == expense2['id']:
        print("\n✅ SUCCESS: Idempotency working correctly!")
        print(f"Both requests returned expense ID {expense1['id']}")
        print(f"Original amount preserved: ${expense1['amount_cents']/100:.2f}")
        return True
    else:
        print("\n❌ FAILURE: Idempotency not working!")
        print(f"First request ID: {expense1['id']}")
        print(f"Second request ID: {expense2['id']}")
        return False

if __name__ == "__main__":
    try:
        test_idempotency()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure backend is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")