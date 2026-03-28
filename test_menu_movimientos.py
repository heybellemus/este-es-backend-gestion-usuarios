#!/usr/bin/env python3
import requests
import json

# Configuración
BASE_URL = "http://127.0.0.1:8000"
TOKEN_URL = f"{BASE_URL}/login/"
MOVIMIENTOS_URL = f"{BASE_URL}/api/menu-movimientos/"

# Datos de prueba para obtener token
login_data = {
    "email": "admin@ejemplo.com",  # Usuario válido de la BD
    "password": "admin123"         # Esta contraseña necesita ser verificada
}

print("=== Probando endpoint MenuMovimientos ===")

# 1. Obtener token JWT
print("\n1. Obteniendo token JWT...")
try:
    response = requests.post(TOKEN_URL, json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access')
        print(f"Token obtenido: {access_token[:20]}...")
        
        # 2. Probar crear movimiento
        print("\n2. Creando movimiento...")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        movimiento_data = {
            "id_producto": 37,
            "id_lote": 47,
            "id_tipo_movimiento": 4,
            "cantidad_movimiento": 2,
            "precio_unitario_movimiento": "15.00",
            "motivo_movimiento": "AJUSTE",
            "documento_referencia_movimiento": "FAC-00123",
            "observaciones_movimiento": "AJUSTE TENIA 43-2 TENGO AHORA 41"
        }
        
        print(f"Datos enviados: {json.dumps(movimiento_data, indent=2)}")
        
        response = requests.post(MOVIMIENTOS_URL, json=movimiento_data, headers=headers)
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Movimiento creado exitosamente!")
            print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
        else:
            print("❌ Error al crear movimiento")
            print(f"Respuesta: {response.text}")
            
    else:
        print("❌ Error al obtener token")
        print(f"Respuesta: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
