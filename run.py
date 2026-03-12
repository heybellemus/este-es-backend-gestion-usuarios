#!/usr/bin/env python
import os
import sys
import socket
import webbrowser

def get_ip():
    """Obtiene la IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '192.168.0.9'

def main():
    """Inicia el servidor Django"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    
    local_ip = get_ip()
    port = 8000
    
    print("\n" + "="*60)
    print("🚀 SERVIDOR DJANGO - DESARROLLO")
    print("="*60)
    print(f"📍 IP Local:      {local_ip}")
    print(f"🔗 URLs de acceso:")
    print(f"   • Local:      http://127.0.0.1:{port}")
    print(f"   • Red:        http://{local_ip}:{port}")
    print(f"   • Red (fija): http://192.168.0.9:{port}")
    print("\n📱 Desde tu móvil usa:")
    print(f"   http://{local_ip}:{port}/api/")
    print("="*60 + "\n")
    
    print("✅ Configuración CORS activada para:")
    print(f"   • http://{local_ip}:3000 (Frontend React)")
    print(f"   • http://{local_ip}:5173 (Frontend Vite)")
    print(f"   • http://localhost:3000")
    print("="*60 + "\n")
    
    # Abrir en navegador automáticamente
    try:
        webbrowser.open(f"http://127.0.0.1:{port}")
    except:
        pass
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])

if __name__ == "__main__":
    main()