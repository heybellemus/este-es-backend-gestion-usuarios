#!/usr/bin/env python
"""
Script para probar login con usuarios reales
"""
import os
import sys
import django
import hashlib

# Agregar el path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from mi_app.models import Usuarios

def hash_password(password):
    """Convierte password a SHA256 como lo hace el frontend"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest().upper()

def test_login():
    print("🔐 Probando login con usuarios reales...")
    
    # Usuarios para probar
    test_cases = [
        ("heybel1lemus@gmail.com", "1327noteveo"),  # Usuario del frontend
        ("maria.garcia@empresa.com", "password123"),  # Usuario de prueba
        ("admin@ejemplo.com", "admin123"),  # Admin de prueba
    ]
    
    for email, password in test_cases:
        print(f"\n{'='*50}")
        print(f"Probando: {email}")
        print(f"Password: {password}")
        print(f"Password hash: {hash_password(password)}")
        
        try:
            usuario = Usuarios.objects.get(email=email)
            print(f"✅ Usuario encontrado: {usuario.nombre} {usuario.apellido}")
            print(f"🔑 Stored hash: {usuario.passwordhash}")
            
            # Verificar si el password coincide
            incoming_hash = hash_password(password)
            stored_hash = (usuario.passwordhash or "").strip().upper()
            
            if incoming_hash == stored_hash:
                print("✅ Password correcto!")
            else:
                print("❌ Password incorrecto")
                print(f"Expected: {incoming_hash}")
                print(f"Got:      {stored_hash}")
                
        except Usuarios.DoesNotExist:
            print("❌ Usuario no encontrado")
    
    # Mostrar passwords de ejemplo para usuarios reales
    print(f"\n{'='*50}")
    print("📋 Usuarios disponibles para pruebas:")
    
    usuarios = Usuarios.objects.filter(activo=True)[:5]
    for usuario in usuarios:
        print(f"\n👤 {usuario.nombre} {usuario.apellido}")
        print(f"   Email: {usuario.email}")
        print(f"   Hash:  {usuario.passwordhash}")
        print(f"   Para probar, necesitas el password original que generó este hash")

if __name__ == "__main__":
    test_login()
