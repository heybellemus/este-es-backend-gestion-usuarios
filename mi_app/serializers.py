# mi_app/serializers.py
from rest_framework import serializers
from .models import Clientes

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = '__all__'
        # O especificar campos manualmente:
        # fields = ['clientid', 'tipodocumento', 'numerodocumento', 'razonsocial', ...]


# Serializer para Departamentos
from .models import Departamentos

class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamentos
        fields = '__all__'

from .models import Roles

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

from .models import Usuarios

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

from .models import Permisos

class PermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permisos
        fields = '__all__'

from .models import RolPermisos

class RolPermisosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPermisos
        fields = '__all__'

from .models import SesionesQR
class SesionesQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = SesionesQR
        fields = '__all__'

from .models import Pantallas

class PantallasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pantallas
        fields = '__all__'

from .models import RolPantallas

class RolPantallasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolPantallas
        fields = '__all__'

# Serializer para Password Reset Token
from .models import PasswordResetToken
class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = ['tokenid', 'usuarioid', 'token', 'email', 'fecha_creacion', 'fecha_expiracion', 'utilizado', 'fecha_utilizacion']
        read_only_fields = ['tokenid', 'fecha_creacion', 'fecha_utilizacion']

# Serializer para solicitud de recuperación
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        return value.strip().lower()

# Serializer para restablecer contraseña
class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return attrs
    
    def validate_token(self, value):
        try:
            token_obj = PasswordResetToken.objects.get(token=value)
            if not token_obj.is_valid:
                raise serializers.ValidationError("Token inválido o expirado.")
            return value
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Token inválido.")

from .models import (
    MenuCategorias,
    MenuUnidadesMedida,
    MenuProductos,
    MenuLotes,
    MenuHistorialPrecios,
    MenuProveedores,
    CatTiposMovimiento,
)


class MenuCategoriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategorias
        fields = '__all__'


class MenuUnidadesMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuUnidadesMedida
        fields = '__all__'


class MenuProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuProductos
        fields = '__all__'


class MenuLotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLotes
        fields = '__all__'




class MenuHistorialPreciosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuHistorialPrecios
        fields = '__all__'


class CatTiposMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposMovimiento
        fields = '__all__'


class MenuProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuProveedores
        fields = '__all__'
