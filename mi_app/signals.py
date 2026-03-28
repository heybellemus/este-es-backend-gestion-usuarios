# mi_app/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import MenuLotes, MenuMovimientos, MenuProductos, CatTiposMovimiento


# =============================================
# TRIGGER 1: Actualizar stock al insertar lotes (Ahora manejado por SQL Server)
# =============================================

@receiver(pre_save, sender=MenuLotes)
def validar_fecha_vencimiento_lote(sender, instance, **kwargs):
    """
    Validar que no se inserten lotes con fechas de vencimiento pasadas
    """
    if instance.fecha_vencimiento_lote and instance.fecha_vencimiento_lote < timezone.now().date():
        raise ValidationError('No se puede insertar un lote con fecha de vencimiento pasada.')


@receiver(post_save, sender=MenuLotes)
def crear_movimiento_entrada_lote(sender, instance, created, **kwargs):
    """
    Crear automáticamente un movimiento de entrada cuando se crea un lote
    con el usuario_id correcto
    """
    # En este proyecto los movimientos/stock se manejan (principalmente) con triggers de SQL Server.
    # Si el trigger está activo, evitar duplicar la inserción desde Django.
    #
    # Para forzar la creación desde Django (sin triggers), define:
    # MENU_MOVIMIENTOS_BY_TRIGGER = False en settings.py
    if getattr(settings, "MENU_MOVIMIENTOS_BY_TRIGGER", True):
        return

    if not created:
        return
    
    # Obtener usuario_id del contexto (pasado desde el ViewSet)
    usuario_id = getattr(instance, '_usuario_id', None)
    if not usuario_id:
        # Si no se proporcionó usuario_id, usar un valor por defecto
        usuario_id = 1
    
    try:
        # Buscar el tipo de movimiento "ENTRADA"
        tipo_entrada = CatTiposMovimiento.objects.filter(codigo_tipo='ENTRADA').first()
        
        # Crear el movimiento de entrada
        MenuMovimientos.objects.create(
            id_producto=instance.id_producto,
            id_lote=instance,
            tipo_movimiento='ENTRADA',
            cantidad_movimiento=instance.cantidad_recibida_lote,
            precio_unitario_movimiento=instance.precio_compra_lote,
            motivo_movimiento=f'Entrada automática por lote {instance.numero_lote or instance.id_lote}',
            id_tipo_movimiento=tipo_entrada,
            usuario_id=usuario_id
        )
    except Exception as e:
        # Log del error pero no levantar excepción para no afectar la creación del lote
        print(f"Error al crear movimiento automático: {e}")


# Nota: La actualización de stock y creación automática de movimientos
# ahora es manejada por el trigger trg_AfterInsertLote en SQL Server
# Mantenemos solo validaciones en Django


# =============================================
# TRIGGER 2: Actualizar stock al insertar movimientos (Ahora manejado por SQL Server)
# =============================================

@receiver(pre_save, sender=MenuMovimientos)
def validar_stock_suficiente(sender, instance, **kwargs):
    """
    Validar stock suficiente para movimientos de salida
    """
    if not instance.id_producto:
        return
        
    # Tipos de movimiento que restan stock (basado en cat_tipos_movimiento)
    tipos_salida = ['VENTA', 'TRANSFERENCIA', 'AJUSTE-', 'DEVOLUCION_P']
    
    if instance.tipo_movimiento in tipos_salida:
        producto = instance.id_producto
        stock_actual = producto.stock_actual_producto or 0
        
        if stock_actual - instance.cantidad_movimiento < 0:
            raise ValidationError(f'Stock insuficiente para el producto ID: {producto.id_producto}. Stock actual: {stock_actual}, requerido: {instance.cantidad_movimiento}')


# Nota: La actualización de stock basada en el signo del catálogo
# ahora es manejada por el trigger trg_AfterInsertMovimiento en SQL Server


# =============================================
# TRIGGER OPCIONAL: Validar actualizaciones directas de stock
# =============================================

@receiver(pre_save, sender=MenuProductos)
def prevenir_actualizacion_directa_stock(sender, instance, **kwargs):
    """
    Prevenir actualización directa del campo stock_actual_producto
    """
    if instance.pk:  # Es una actualización, no una creación
        try:
            original = MenuProductos.objects.get(pk=instance.pk)
            if original.stock_actual_producto != instance.stock_actual_producto:
                # Verificar si la llamada viene de un contexto permitido (signals)
                import inspect
                frame = inspect.currentframe()
                caller_frame = frame.f_back.f_back
                caller_name = caller_frame.f_code.co_name if caller_frame else ''
                
                # Permitir solo si viene de métodos relacionados con actualización de stock
                if not any(name in caller_name for name in ['actualizar_stock', 'signal', '_update_stock']):
                    raise ValidationError('No se permite actualizar stock_actual_producto directamente. Use movimientos o lotes.')
                    
        except MenuProductos.DoesNotExist:
            # Es un nuevo registro, permitimos
            pass
