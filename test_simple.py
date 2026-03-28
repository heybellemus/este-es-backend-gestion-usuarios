#!/usr/bin/env python3
import requests
import json

# Simple prueba del endpoint de login
BASE_URL = "http://127.0.0.1:8000"
TOKEN_URL = f"{BASE_URL}/login/"

login_data = {
    "email": "admin@ejemplo.com",
    "password": "admin123"
}

print("=== Probando login ===")
try:
    response = requests.post(TOKEN_URL, json=login_data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
