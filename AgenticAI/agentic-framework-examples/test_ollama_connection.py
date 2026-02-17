#!/usr/bin/env python
"""
Ollama Connection Test Script
==============================
Tests connection to Ollama server and lists available chat and embedding models.
"""

import os
import socket
import sys
from urllib.parse import urlparse

import requests

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3.1")
OLLAMA_EMBEDDING_MODEL = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")


def test_dns_resolution(hostname):
    """Test if hostname can be resolved to IP address."""
    print(f"1. Testing DNS resolution for '{hostname}'...")
    try:
        ip = socket.gethostbyname(hostname)
        print(f"   ✓ Resolved to {ip}")
        return True
    except socket.gaierror as e:
        print(f"   ✗ DNS resolution failed: {e}")
        return False


def test_port_connection(hostname, port):
    """Test if port is reachable."""
    print(f"2. Testing port {port} connection...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = sock.connect_ex((hostname, port))
        sock.close()
        if result == 0:
            print(f"   ✓ Port {port} is open")
            return True
        else:
            print(f"   ✗ Port {port} is closed or unreachable")
            return False
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        return False


def test_http_connection(url, api_key):
    """Test HTTP/HTTPS connection and authentication."""
    parsed = urlparse(url)
    protocol = parsed.scheme
    print(f"3. Testing {protocol.upper()} connection to {url}...")
    
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.get(f"{url}/api/tags", headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"   ✓ {protocol.upper()} connection successful")
            return True, response.json()
        elif response.status_code == 401:
            print(f"   ✗ Authentication failed (401)")
            return False, None
        else:
            print(f"   ✗ HTTP error {response.status_code}")
            return False, None
    except requests.exceptions.SSLError as e:
        print(f"   ✗ SSL/TLS error: {e}")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection failed: {e}")
        return False, None


def check_authentication(api_key):
    """Check if API key is configured."""
    print("4. Checking authentication...")
    if api_key:
        print(f"   ✓ API key configured (length: {len(api_key)})")
    else:
        print("   ℹ No API key configured (not required for local Ollama)")


def list_models(models_data):
    """List available chat and embedding models."""
    if not models_data or "models" not in models_data:
        print("\n✗ No models found")
        return
    
    models = models_data["models"]
    
    chat_models = []
    embed_models = []
    
    for model in models:
        name = model.get("name", "")
        if "embed" in name.lower():
            embed_models.append(name)
        else:
            chat_models.append(name)
    
    print(f"\n{'='*60}")
    print(f"Available Models ({len(models)} total)")
    print(f"{'='*60}")
    
    print(f"\nChat Models ({len(chat_models)}):")
    for model in chat_models:
        print(f"  • {model}")
    
    print(f"\nEmbedding Models ({len(embed_models)}):")
    for model in embed_models:
        print(f"  • {model}")
    
    # Check if required models are available
    print(f"\n{'='*60}")
    print("Required Models Check")
    print(f"{'='*60}")
    
    all_model_names = [m.get("name", "") for m in models]
    
    chat_found = any(OLLAMA_CHAT_MODEL in name for name in all_model_names)
    if chat_found:
        print(f"✓ Chat model '{OLLAMA_CHAT_MODEL}' is available")
    else:
        print(f"⚠ WARNING: Chat model '{OLLAMA_CHAT_MODEL}' NOT found!")
        print(f"  Run: ollama pull {OLLAMA_CHAT_MODEL}")
    
    embed_found = any(OLLAMA_EMBEDDING_MODEL in name for name in all_model_names)
    if embed_found:
        print(f"✓ Embedding model '{OLLAMA_EMBEDDING_MODEL}' is available")
    else:
        print(f"⚠ WARNING: Embedding model '{OLLAMA_EMBEDDING_MODEL}' NOT found!")
        print(f"  Run: ollama pull {OLLAMA_EMBEDDING_MODEL}")


def main():
    print(f"{'='*60}")
    print("Ollama Server Connection Test")
    print(f"{'='*60}")
    print(f"Server URL: {OLLAMA_BASE_URL}\n")
    
    parsed_url = urlparse(OLLAMA_BASE_URL)
    hostname = parsed_url.hostname or "localhost"
    port = parsed_url.port or (443 if parsed_url.scheme == "https" else 11434)
    
    # Test 1: DNS Resolution
    if not test_dns_resolution(hostname):
        sys.exit(1)
    
    # Test 2: Port Connection
    if not test_port_connection(hostname, port):
        sys.exit(1)
    
    # Test 3: HTTP/HTTPS Connection
    success, models_data = test_http_connection(OLLAMA_BASE_URL, OLLAMA_API_KEY)
    if not success:
        sys.exit(1)
    
    # Test 4: Authentication Check
    check_authentication(OLLAMA_API_KEY)
    
    # List Models
    list_models(models_data)
    
    print(f"\n{'='*60}")
    print("✓ All tests passed!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
