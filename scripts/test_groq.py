#!/usr/bin/env python3
"""
Test script to verify Groq API key and model works
"""
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from config import GROQ_API_KEY

def test_groq():
    """Test Groq API connection and model"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        print("Testing Groq API connection...")
        print(f"Using API key: {GROQ_API_KEY[:20]}...")
        
        # Simple test completion
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'Hello, Groq is working!' and nothing else."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"\n✓ Success! Model response: {result}")
        print(f"✓ Model: {response.model}")
        print(f"✓ Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_groq()
    sys.exit(0 if success else 1)

