#!/usr/bin/env python
"""
Script para probar el login después de corregir passwords
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_login(email, password):
    """Prueba login con credenciales específicas"""
    url = f"{BASE_URL}/login/"
    data = {"email": email, "password": password}
    
    try:
        response = requests.post(url, json=data)
        
        print(f"\n{'='*50}")
        print(f"Probando login: {email}")
        print(f"Password: {password}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login exitoso!")
            print(f"Usuario: {result['usuario']['nombre']} {result['usuario']['apellido']}")
            print(f"Rol ID: {result['usuario']['rolid']}")
            print(f"Access token: {result['access'][:50]}...")
            return result['access']
        else:
            print("❌ Login fallido")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def test_apis_with_token(token):
    """Prueba algunas APIs con el token obtenido"""
    if not token:
        print("\n❌ No se puede probar APIs sin token")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Probar endpoints principales
    endpoints = [
        "/api/clientes/",
        "/api/usuarios/",
        "/api/menu-productos/",
    ]
    
    print(f"\n{'='*50}")
    print("🔐 Probando APIs con token JWT")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            
            print(f"\nGET {endpoint}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ OK ({len(data)} registros)")
                else:
                    print("✅ OK")
            else:
                print("❌ ERROR")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    print("🚀 Probando login y APIs después de corrección")
    
    # Probar login con los usuarios corregidos
    test_cases = [
        ("heybel1lemus@gmail.com", "1327noteveo"),
        ("admin@ejemplo.com", "admin123"),
    ]
    
    token = None
    for email, password in test_cases:
        token = test_login(email, password)
        if token:
            break
    
    # Si tenemos token, probar APIs
    if token:
        test_apis_with_token(token)
    
    print(f"\n{'='*50}")
    print("🏁 Pruebas completadas")

if __name__ == "__main__":
    main()
