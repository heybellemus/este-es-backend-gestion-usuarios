#!/usr/bin/env python
"""
Script para verificar usuarios en la base de datos
"""
import os
import sys
import django

# Agregar el path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from mi_app.models import Usuarios

def main():
    print("🔍 Verificando usuarios en la base de datos...")
    
    try:
        usuarios = Usuarios.objects.all()
        
        if not usuarios.exists():
            print("❌ No hay usuarios en la base de datos")
            return
        
        print(f"📊 Total de usuarios: {usuarios.count()}")
        print("\n👥 Lista de usuarios:")
        
        for usuario in usuarios:
            print(f"  - ID: {usuario.usuarioid}")
            print(f"    Email: {usuario.email}")
            print(f"    Nombre: {usuario.nombre} {usuario.apellido}")
            print(f"    Activo: {usuario.activo}")
            print(f"    Rol ID: {usuario.rolid_id}")
            print("-" * 40)
            
        # Mostrar usuarios activos
        activos = Usuarios.objects.filter(activo=True)
        print(f"\n✅ Usuarios activos: {activos.count()}")
        
        if activos.exists():
            print("\n🔑 Puedes usar estos credenciales para probar el login:")
            for usuario in activos[:3]:  # Mostrar solo los primeros 3
                print(f"  Email: {usuario.email}")
                print(f"  Password hash: {usuario.passwordhash[:20]}...")
                print("-" * 30)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
