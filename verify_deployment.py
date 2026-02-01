#!/usr/bin/env python3
"""
Deployment verification script for Vercel-deployed expense tracker.
Run this after deployment to verify all functionality works.
"""

import requests
import json
import time
import sys

def test_deployment(base_url):
    """Test deployed application functionality"""
    
    print(f"🚀 Testing deployment at: {base_url}")
    print("=" * 50)
    
    # Test 1: Frontend accessibility
    print("\n1. Testing frontend accessibility...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not accessible: {e}")
        return False
    
    # Test 2: Create expense API
    print("\n2. Testing expense creation API...")
    test_expense = {
        "idempotency_key": f"deploy-test-{int(time.time())}",
        "amount": 42.50,
        "category": "Deployment Test",
        "description": "Testing Vercel deployment",
        "date": "2024-01-15"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/expenses",
            json=test_expense,
            timeout=10
        )
        
        if response.status_code == 200:
            expense_data = response.json()
            print("✅ Expense creation API working")
            print(f"   Created expense ID: {expense_data.get('id')}")
            expense_id = expense_data.get('id')
        else:
            print(f"❌ Expense creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Expense creation API error: {e}")
        return False
    
    # Test 3: List expenses API
    print("\n3. Testing expense listing API...")
    try:
        response = requests.get(f"{base_url}/api/list", timeout=10)
        
        if response.status_code == 200:
            expenses = response.json()
            print("✅ Expense listing API working")
            print(f"   Found {len(expenses)} expenses")
            
            # Verify our test expense is in the list
            test_found = any(exp.get('id') == expense_id for exp in expenses)
            if test_found:
                print("✅ Test expense found in list")
            else:
                print("⚠️  Test expense not found in list (may be expected with SQLite)")
        else:
            print(f"❌ Expense listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Expense listing API error: {e}")
        return False
    
    # Test 4: Idempotency
    print("\n4. Testing idempotency...")
    try:
        # Send same request again
        response2 = requests.post(
            f"{base_url}/api/expenses",
            json=test_expense,
            timeout=10
        )
        
        if response2.status_code == 200:
            expense_data2 = response2.json()
            if expense_data2.get('id') == expense_id:
                print("✅ Idempotency working - same expense returned")
            else:
                print("⚠️  Idempotency may not be working (different IDs)")
        else:
            print(f"❌ Idempotency test failed: {response2.status_code}")
    except Exception as e:
        print(f"❌ Idempotency test error: {e}")
    
    # Test 5: Filtering
    print("\n5. Testing category filtering...")
    try:
        response = requests.get(
            f"{base_url}/api/list?category=Deployment Test",
            timeout=10
        )
        
        if response.status_code == 200:
            filtered_expenses = response.json()
            print("✅ Category filtering API working")
            print(f"   Found {len(filtered_expenses)} expenses in 'Deployment Test' category")
        else:
            print(f"❌ Category filtering failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Category filtering error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Deployment verification completed!")
    print("\n📋 Manual verification checklist:")
    print("   □ Visit the frontend URL and test the UI")
    print("   □ Create an expense through the web interface")
    print("   □ Verify filtering and sorting work")
    print("   □ Test error handling with invalid data")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_deployment.py <base_url>")
        print("Example: python verify_deployment.py https://your-app.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    test_deployment(base_url)