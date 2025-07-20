#!/usr/bin/env python3
"""
Test script for the POS CX Voice Assistant endpoint
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployed URL
CHAT_ENDPOINT = f"{BASE_URL}/chat"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a sample conversation"""
    
    # Sample conversation flow
    conversation = [
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": "I want to schedule a meeting"},
        {"role": "user", "content": "My name is John Doe"},
        {"role": "user", "content": "My phone number is 555-123-4567"},
        {"role": "user", "content": "I'd like to meet on Monday at 2 PM"},
        {"role": "user", "content": "Yes, that's correct"}
    ]
    
    print("\n🧪 Testing conversation flow...")
    
    for i, message in enumerate(conversation, 1):
        print(f"\n--- Step {i}: {message['content']} ---")
        
        try:
            # Build messages array with conversation history
            messages = conversation[:i]
            
            response = requests.post(
                CHAT_ENDPOINT,
                json={"messages": messages},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result['message']}")
                
                # Check for expected patterns
                if i == 1 and "Skylar" in result['message']:
                    print("✅ Correct greeting detected")
                elif i == 2 and ("name" in result['message'].lower() or "help" in result['message'].lower()):
                    print("✅ Correct intent detection")
                elif i == 3 and "phone" in result['message'].lower():
                    print("✅ Correct name collection")
                elif i == 4 and "time" in result['message'].lower():
                    print("✅ Correct phone collection")
                elif i == 5 and "confirm" in result['message'].lower():
                    print("✅ Correct scheduling")
                elif i == 6 and ("awesome" in result['message'].lower() or "set" in result['message'].lower()):
                    print("✅ Correct confirmation")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        # Small delay between requests
        time.sleep(1)

def test_retell_format():
    """Test with Retell-compatible format"""
    print("\n🔗 Testing Retell-compatible format...")
    
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={
                "messages": [
                    {"role": "user", "content": "Hello, I need to schedule a meeting"}
                ],
                "stream": False
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Retell format works: {result['message'][:100]}...")
            
            # Check response structure
            if 'message' in result and 'usage' in result:
                print("✅ Response structure is correct")
            else:
                print("❌ Response structure is missing required fields")
        else:
            print(f"❌ Retell format test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Retell format test failed: {e}")

if __name__ == "__main__":
    print("🚀 POS CX Voice Assistant - Endpoint Test (Gemini 2.0 Flash)")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("❌ Server is not running. Please start the server first:")
        print("   python main.py")
        exit(1)
    
    # Test chat endpoint
    test_chat_endpoint()
    
    # Test Retell format
    test_retell_format()
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")
    print("\n📋 Next steps:")
    print("1. Deploy to a cloud platform (Railway, Render, Heroku)")
    print("2. Get your public URL")
    print("3. Configure in Retell dashboard")
    print("4. Test with actual voice calls") 