#!/usr/bin/env python
import requests
import json

# URL del endpoint de login
LOGIN_URL = "http://127.0.0.1:8000/login/"

# Casos de prueba
test_cases = [
    {
        "name": "Usuario admin con hash correcto",
        "data": {
            "email": "admin@ejemplo.com",
            "password": "240BE518FABD2724DDB6F04EEB1DA5967448D7E831C08C8FA822809F74C720A9"
        }
    },
    {
        "name": "Usuario con password incorrecto",
        "data": {
            "email": "admin@ejemplo.com",
            "password": "password_incorrecto"
        }
    },
    {
        "name": "Usuario que no existe",
        "data": {
            "email": "noexiste@ejemplo.com",
            "password": "cualquier_password"
        }
    },
    {
        "name": "Datos incompletos (solo email)",
        "data": {
            "email": "admin@ejemplo.com"
        }
    }
]

def test_login_api():
    print("🧪 Probando API de Login")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                LOGIN_URL,
                headers={"Content-Type": "application/json"},
                json=test_case["data"],
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Login exitoso")
                try:
                    response_data = response.json()
                    if 'access' in response_data and 'refresh' in response_data:
                        print("✅ Tokens JWT generados correctamente")
                        print(f"👤 Usuario: {response_data.get('usuario', {}).get('nombreusuario', 'N/A')}")
                    else:
                        print("⚠️ Response no contiene tokens esperados")
                except json.JSONDecodeError:
                    print("⚠️ Response no es JSON válido")
            elif response.status_code == 401:
                print("❌ Credenciales inválidas (esperado para este test)")
            elif response.status_code == 400:
                print("❌ Datos inválidos o incompletos (esperado para este test)")
            else:
                print(f"⚠️ Status code inesperado: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_login_api()
