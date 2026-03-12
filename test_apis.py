#!/usr/bin/env python
"""
Script para probar las APIs principales del backend Django
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoint(endpoint, method="GET", data=None, headers=None):
    """Prueba un endpoint específico"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"Método {method} no soportado")
            return False
            
        print(f"\n{'='*50}")
        print(f"Probando: {method} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ OK")
            if response.json():
                print(f"Response: {json.dumps(response.json(), indent=2)[:200]}...")
        else:
            print("❌ ERROR")
            print(f"Response: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ No se pudo conectar a {url}")
        print("Asegúrate de que el servidor Django esté corriendo en localhost:8000")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de APIs Django")
    print("Asegúrate de que el servidor esté corriendo: python manage.py runserver")
    
    # Pruebas básicas (sin autenticación)
    tests = [
        ("/", "GET"),
        ("/api/", "GET"),
        ("/login/", "POST", {"email": "test@test.com", "password": "test123"}),
    ]
    
    print("\n📋 Probando endpoints públicos...")
    
    for test in tests:
        if len(test) == 2:
            endpoint, method = test
            test_api_endpoint(endpoint, method)
        else:
            endpoint, method, data = test
            test_api_endpoint(endpoint, method, data)
    
    print(f"\n{'='*50}")
    print("🏁 Pruebas completadas")
    print("\n📝 Nota:")
    print("- Los endpoints que requieren autenticación (/api/*) necesitarán un token JWT")
    print("- El login requiere credenciales válidas de la base de datos")
    print("- Para probar endpoints autenticados, primero obtén un token JWT")

if __name__ == "__main__":
    main()
