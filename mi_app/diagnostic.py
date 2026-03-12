# mi_app/diagnostic.py
from django.db import connection
import traceback

def diagnosticar_modelo_usuario():
    print("=== DIAGNÓSTICO MODELO USUARIO ===")
    
    # 1. Verificar conexión
    print("\n1. Verificando conexión...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DB_NAME()")
            db_name = cursor.fetchone()[0]
            print(f"   ✓ Conectado a: {db_name}")
    except Exception as e:
        print(f"   ✗ Error conexión: {e}")
        return
    
    # 2. Verificar tabla existe
    print("\n2. Verificando existencia de tabla...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' 
                AND TABLE_NAME = 'Usuarios'
            """)
            exists = cursor.fetchone()[0]
            print(f"   ✓ Tabla existe: {'Sí' if exists > 0 else 'No'}")
    except Exception as e:
        print(f"   ✗ Error verificando tabla: {e}")
    
    # 3. Verificar columnas
    print("\n3. Verificando columnas...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'dbo' 
                AND TABLE_NAME = 'Usuarios'
                ORDER BY ORDINAL_POSITION
            """)
            columnas = cursor.fetchall()
            print(f"   ✓ Columnas encontradas: {len(columnas)}")
            for col in columnas[:5]:  # Mostrar primeras 5
                print(f"     - {col[0]} ({col[1]}, nullable: {col[2]})")
    except Exception as e:
        print(f"   ✗ Error verificando columnas: {e}")
    
    # 4. Intentar consulta directa
    print("\n4. Consulta directa SQL...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT TOP 3 UsuarioID, NombreUsuario FROM dbo.Usuarios")
            resultados = cursor.fetchall()
            print(f"   ✓ Registros encontrados: {len(resultados)}")
            for row in resultados:
                print(f"     - ID: {row[0]}, Usuario: {row[1]}")
    except Exception as e:
        print(f"   ✗ Error consulta directa: {e}")
        traceback.print_exc()
    
    # 5. Probar ORM de Django
    print("\n5. Probando ORM de Django...")
    try:
        from .models import Usuarios
        print(f"   ✓ Modelo importado: {Usuarios}")
        
        try:
            count = Usuarios.objects.count()
            print(f"   ✓ Count() funciona: {count} registros")
        except Exception as e:
            print(f"   ✗ Error en count(): {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"   ✗ Error importando modelo: {e}")
        traceback.print_exc()

# Para ejecutar:
# python manage.py shell
# from mi_app.diagnostic import diagnosticar_modelo_usuario
# diagnosticar_modelo_usuario()python manage.py shell