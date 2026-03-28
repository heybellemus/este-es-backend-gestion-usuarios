# mi_app/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
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
    MenuHistorialPrecios,
    MenuLotes,
    MenuMovimientos,
    MenuProductos,
    MenuProveedores,
    MenuUnidadesMedida,
    CatTiposMovimiento,
)

from django.utils import timezone

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
        read_only_fields = ('stock_actual_producto',)  # Stock actual es solo lectura, se actualiza via triggers


class MenuLotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuLotes
        fields = '__all__'
    
    def validate(self, data):
        try:
            # Validar fecha de vencimiento
            if data.get('fecha_vencimiento_lote') and data['fecha_vencimiento_lote'] < timezone.now().date():
                raise ValidationError('No se puede insertar un lote con fecha de vencimiento pasada.')
            return data
        except ValidationError as e:
            raise serializers.ValidationError(str(e))


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


class MenuMovimientosSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuMovimientos
        fields = '__all__'
        read_only_fields = ('usuario_id', 'nombre_usuario')  # Se asignan automáticamente en el viewset
    
    def validate(self, data):
        try:
            # Validar stock suficiente para movimientos de salida
            if data.get('id_producto') and data.get('tipo_movimiento') and data.get('cantidad_movimiento'):
                tipos_salida = ['VENTA', 'TRANSFERENCIA', 'AJUSTE-', 'DEVOLUCION_P']
                
                if data['tipo_movimiento'] in tipos_salida:
                    producto = data['id_producto']
                    stock_actual = producto.stock_actual_producto or 0
                    
                    if stock_actual - data['cantidad_movimiento'] < 0:
                        raise ValidationError(
                            f'Stock insuficiente para el producto ID: {producto.id_producto}. '
                            f'Stock actual: {stock_actual}, requerido: {data["cantidad_movimiento"]}'
                        )
            
            return data
        except ValidationError as e:
            raise serializers.ValidationError(str(e))


# Serializer para solicitud de salida PEPS
class SalidaPEPSSerializer(serializers.Serializer):
    id_producto = serializers.IntegerField(required=True)
    cantidad_a_descontar = serializers.IntegerField(required=True, min_value=1)
    id_tipo_movimiento = serializers.IntegerField(required=True)
    motivo = serializers.CharField(max_length=255, required=False, allow_blank=True)


# Serializer para procesamiento de mermas
class ProcesarMermasSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField(required=True)
