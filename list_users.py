#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from mi_app.models import Usuarios

print("=== Usuarios en la base de datos ===")
try:
    usuarios = Usuarios.objects.all()
    for usuario in usuarios:
        print(f"ID: {usuario.usuarioid}, Email: {usuario.email}, Nombre: {usuario.nombre} {usuario.apellido}, Usuario: {usuario.nombreusuario}")
        
    if not usuarios:
        print("No se encontraron usuarios en la base de datos.")
        
except Exception as e:
    print(f"Error: {e}")
