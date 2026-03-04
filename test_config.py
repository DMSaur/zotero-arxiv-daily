#!/usr/bin/env python3
"""Test script to verify configuration before running main.py"""
import os
import sys

print("=" * 50)
print("CONFIGURATION TEST")
print("=" * 50)

# Check environment variables
env_vars = [
    'ZOTERO_ID',
    'ZOTERO_KEY',
    'SENDER',
    'RECEIVER',
    'SENDER_PASSWORD',
    'OPENAI_API_KEY',
    'OPENAI_API_BASE',
    'DEBUG',
]

print("\n1. Environment Variables:")
for var in env_vars:
    value = os.environ.get(var, 'NOT SET')
    if value != 'NOT SET':
        # Mask sensitive values
        masked = value[:4] + '***' + value[-4:] if len(value) > 8 else '***'
        print(f"   [OK] {var}={masked}")
    else:
        print(f"   [MISSING] {var}")

# Check custom.yaml
print("\n2. Custom Config File:")
if os.path.exists('config/custom.yaml'):
    with open('config/custom.yaml', 'r') as f:
        content = f.read()
        print("   [OK] File exists")
        print("\n   Content:")
        for line in content.split('\n'):
            print(f"   {line}")
else:
    print("   [ERROR] File does not exist")

# Test OpenAI client initialization
print("\n3. OpenAI Client Test:")
try:
    from openai import OpenAI
    api_key = os.environ.get('OPENAI_API_KEY', '')
    base_url = os.environ.get('OPENAI_API_BASE', '')

    if not api_key:
        print("   [ERROR] OPENAI_API_KEY is empty")
    elif not base_url:
        print("   [ERROR] OPENAI_API_BASE is empty")
    else:
        print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
        print(f"   Base URL: {base_url}")

        # Try to initialize client (don't make actual request)
        client = OpenAI(api_key=api_key, base_url=base_url)
        print("   [OK] Client initialized")

        # Try a simple test request
        print("\n4. API Connection Test:")
        try:
            # Use a minimal test
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            print(f"   [OK] API connection successful")
            print(f"   Response: {response.choices[0].message.content[:50]}...")
        except Exception as e:
            print(f"   [ERROR] API request failed: {e}")
except ImportError as e:
    print(f"   [ERROR] Cannot import openai: {e}")
except Exception as e:
    print(f"   [ERROR] {e}")

# Test sentence transformers
print("\n5. Sentence Transformers Test:")
try:
    from sentence_transformers import SentenceTransformer
    print("   [OK] Import successful")

    model_name = "jinaai/jina-embeddings-v5-text-nano"
    print(f"   Loading model: {model_name}")
    encoder = SentenceTransformer(model_name, trust_remote_code=True)
    print("   [OK] Model loaded")
except Exception as e:
    print(f"   [ERROR] {e}")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
