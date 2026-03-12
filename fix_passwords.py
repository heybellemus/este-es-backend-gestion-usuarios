#!/usr/bin/env python
"""
Script para corregir passwords de usuarios
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
    """Convierte password a SHA256"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest().upper()

def fix_passwords():
    print("🔧 Corrigiendo passwords de usuarios...")
    
    # Corregir el password de heybel1lemus@gmail.com
    try:
        usuario = Usuarios.objects.get(email="heybel1lemus@gmail.com")
        old_hash = usuario.passwordhash
        
        # Si el password no está hasheado, lo hasheamos
        if old_hash == "1327noteveo":
            new_hash = hash_password("1327noteveo")
            usuario.passwordhash = new_hash
            usuario.save()
            print(f"✅ Password corregido para {usuario.email}")
            print(f"   Antes: {old_hash}")
            print(f"   Después: {new_hash}")
        else:
            print(f"ℹ️  Password ya está hasheado para {usuario.email}")
            
    except Usuarios.DoesNotExist:
        print("❌ Usuario heybel1lemus@gmail.com no encontrado")
    
    # Verificar otros usuarios que puedan tener passwords sin hashear
    print(f"\n🔍 Verificando otros usuarios...")
    usuarios = Usuarios.objects.all()
    
    for usuario in usuarios:
        if not usuario.passwordhash or len(usuario.passwordhash) != 64:
            print(f"⚠️  {usuario.email} tiene password sospechoso: {usuario.passwordhash}")
    
    # Mostrar usuarios para pruebas
    print(f"\n📋 Usuarios para pruebas:")
    print("1. admin@ejemplo.com - password: admin123 ✅")
    print("2. heybel1lemus@gmail.com - password: 1327noteveo ✅ (corregido)")

if __name__ == "__main__":
    fix_passwords()
