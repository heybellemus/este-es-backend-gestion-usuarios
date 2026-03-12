# mi_app/permissions.py
from functools import wraps
from django.http import JsonResponse
from rest_framework.permissions import BasePermission
from .models import Pantallas, RolPantallas, Usuarios


class TieneAccesoPantalla(BasePermission):
    """
    Permission class para verificar si un usuario tiene acceso a una pantalla específica
    """
    
    def __init__(self, codigo_pantalla=None):
        self.codigo_pantalla = codigo_pantalla
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Si no se especifica código de pantalla, denegar acceso
        if not self.codigo_pantalla:
            return False
        
        return usuario_tiene_acceso_pantalla(request.user, self.codigo_pantalla)


def requiere_acceso_pantalla(codigo_pantalla):
    """
    Decorador para verificar si el usuario tiene acceso a una pantalla específica
    Uso: @requiere_acceso_pantalla('clientes_list')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'No autenticado',
                    'mensaje': 'Debe iniciar sesión para acceder a esta pantalla'
                }, status=401)
            
            # Verificar acceso a la pantalla
            if not usuario_tiene_acceso_pantalla(request.user, codigo_pantalla):
                return JsonResponse({
                    'error': 'Acceso denegado',
                    'mensaje': f'No tiene permisos para acceder a la pantalla: {codigo_pantalla}'
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def usuario_tiene_acceso_pantalla(usuario, codigo_pantalla):
    """
    Verifica si un usuario tiene acceso a una pantalla específica
    """
    try:
        # Obtener el usuario real si es un TokenUser de JWT
        if hasattr(usuario, 'id') and not hasattr(usuario, 'usuarioid'):
            usuario_real = Usuarios.objects.get(usuarioid=usuario.id)
        else:
            usuario_real = usuario
        
        # Verificar que el usuario tenga rol asignado
        if not usuario_real.rolid:
            return False
        
        # Buscar la pantalla por código
        try:
            pantalla = Pantallas.objects.get(codigo=codigo_pantalla, activo=True)
        except Pantallas.DoesNotExist:
            return False
        
        # Verificar si el rol tiene acceso a esta pantalla
        acceso = RolPantallas.objects.filter(
            rolid=usuario_real.rolid,
            pantallaid=pantalla.pantallaid,
            acceso=True
        ).exists()
        
        return acceso
        
    except Exception as e:
        print(f"Error verificando acceso a pantalla: {e}")
        return False


def obtener_pantallas_usuario(usuario):
    """
    Obtiene la lista de pantallas a las que un usuario tiene acceso
    """
    try:
        # Obtener el usuario real si es un TokenUser de JWT
        if hasattr(usuario, 'id') and not hasattr(usuario, 'usuarioid'):
            usuario_real = Usuarios.objects.get(usuarioid=usuario.id)
        else:
            usuario_real = usuario
        
        if not usuario_real.rolid:
            return []
        
        # Obtener pantallas accesibles para el rol del usuario
        pantallas_acceso = RolPantallas.objects.filter(
            rolid=usuario_real.rolid,
            acceso=True,
            pantallaid__activo=True
        ).select_related('pantallaid')
        
        return [
            {
                'pantallaid': rp.pantallaid.pantallaid,
                'nombre': rp.pantallaid.nombre,
                'codigo': rp.pantallaid.codigo,
                'descripcion': rp.pantallaid.descripcion,
                'ruta': rp.pantallaid.ruta,
                'modulo': rp.pantallaid.modulo
            }
            for rp in pantallas_acceso
        ]
        
    except Exception as e:
        print(f"Error obteniendo pantallas del usuario: {e}")
        return []


def verificar_acceso_multiple_pantallas(usuario, codigos_pantalla):
    """
    Verifica si un usuario tiene acceso a múltiples pantallas
    Retorna un diccionario con el acceso de cada pantalla
    """
    resultado = {}
    for codigo in codigos_pantalla:
        resultado[codigo] = usuario_tiene_acceso_pantalla(usuario, codigo)
    return resultado
