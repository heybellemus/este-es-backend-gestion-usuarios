# mi_app/admin.py
from django.contrib import admin
from .models import (
    CatTiposMovimiento,
    Clientes,
    Departamentos,
    MenuCategorias,
    MenuHistorialPrecios,
    MenuLotes,
    MenuMovimientos,
    MenuProductos,
    MenuProveedores,
    MenuUnidadesMedida,
    Pantallas,
    PasswordResetToken,
    Permisos,
    Roles,
    RolPantallas,
    RolPermisos,
    SesionesQR,
    Usuarios,
)

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('clienteid', 'razonsocial', 'numerodocumento', 'ciudad', 'activo')
    list_filter = ('activo', 'ciudad', 'pais')
    search_fields = ('razonsocial', 'nombrecomercial', 'numerodocumento', 'email')
    readonly_fields = ('clienteid', 'fechacreacion', 'fechamodificacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('tipodocumento', 'numerodocumento', 'razonsocial', 'nombrecomercial')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'direccion', 'ciudad', 'pais')
        }),
        ('Estado y Auditoría', {
            'fields': ('activo', 'creadopor', 'fechacreacion', 'modificadopor', 'fechamodificacion')
        }),
    )


# Admin para Departamentos
@admin.register(Departamentos)
class DepartamentosAdmin(admin.ModelAdmin):
    list_display = ('departamentoid', 'nombre', 'activo', 'fechacreacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('departamentoid', 'fechacreacion')
  
  # Admin para Roles
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('rolid', 'nombre', 'nivelacceso', 'activo')
    list_filter = ('activo', 'nivelacceso')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('rolid',)

# Admin para Usuarios
@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ('usuarioid', 'nombreusuario', 'email', 'activo', 'rolid', 'departamentoid', 'bloqueado')
    list_filter = ('activo', 'bloqueado', 'rolid', 'departamentoid')
    search_fields = ('nombreusuario', 'email', 'nombre', 'apellido')
    readonly_fields = ('usuarioid', 'fechacreacion', 'fechabloqueo', 'ultimoacceso')

# Admin para Permisos
@admin.register(Permisos)
class PermisosAdmin(admin.ModelAdmin):
    list_display = ('permisoid', 'nombre', 'codigo', 'modulo')
    search_fields = ('nombre', 'codigo', 'modulo')
    readonly_fields = ('permisoid',)

# Admin para RolPermisos
@admin.register(RolPermisos)
class RolPermisosAdmin(admin.ModelAdmin):
    list_display = ('rolpermisoid', 'rolid', 'permisoid', 'otorgado', 'fechaasignacion')
    list_filter = ('otorgado', 'rolid', 'permisoid')
    search_fields = ('rolid__nombre', 'permisoid__nombre')
    readonly_fields = ('rolpermisoid',)

# Admin para Pantallas
@admin.register(Pantallas)
class PantallasAdmin(admin.ModelAdmin):
    list_display = ('pantallaid', 'nombre', 'codigo', 'modulo', 'activo', 'fechacreacion')
    list_filter = ('activo', 'modulo')
    search_fields = ('nombre', 'codigo', 'descripcion', 'ruta')
    readonly_fields = ('pantallaid', 'fechacreacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'codigo', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('ruta', 'modulo', 'activo')
        }),
        ('Auditoría', {
            'fields': ('pantallaid', 'fechacreacion'),
            'classes': ('collapse',)
        }),
    )

# Admin para RolPantallas
@admin.register(RolPantallas)
class RolPantallasAdmin(admin.ModelAdmin):
    list_display = ('rolpantallaid', 'rolid', 'pantallaid', 'acceso', 'fechaasignacion')
    list_filter = ('acceso', 'rolid', 'pantallaid__modulo')
    search_fields = ('rolid__nombre', 'pantallaid__nombre', 'pantallaid__codigo')
    readonly_fields = ('rolpantallaid', 'fechaasignacion')
    
    fieldsets = (
        ('Asignación', {
            'fields': ('rolid', 'pantallaid', 'acceso')
        }),
        ('Auditoría', {
            'fields': ('rolpantallaid', 'fechaasignacion'),
            'classes': ('collapse',)
        }),
    )

# Admin para MenuCategorias
@admin.register(MenuCategorias)
class MenuCategoriasAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre_categoria', 'activo_categoria', 'fecha_creacion_categoria')
    list_filter = ('activo_categoria',)
    search_fields = ('nombre_categoria', 'descripcion_categoria')
    readonly_fields = ('id_categoria',)


# Admin para MenuProveedores
@admin.register(MenuProveedores)
class MenuProveedoresAdmin(admin.ModelAdmin):
    list_display = ('id_proveedor', 'nombre_comercial', 'rtn', 'telefono', 'correo_electronico', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre_comercial', 'rtn', 'persona_contacto', 'correo_electronico')
    readonly_fields = ('id_proveedor', 'fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_comercial', 'rtn', 'persona_contacto')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo_electronico', 'direccion')
        }),
        ('Información Adicional', {
            'fields': ('datos_bancarios', 'observaciones')
        }),
        ('Estado y Auditoría', {
            'fields': ('activo', 'fecha_creacion', 'fecha_modificacion')
        }),
    )


@admin.register(MenuUnidadesMedida)
class MenuUnidadesMedidaAdmin(admin.ModelAdmin):
    list_display = (
        'id_unidad_medida',
        'codigo_unidad',
        'nombre_unidad',
        'simbolo_unidad',
        'activo_unidad',
        'fecha_creacion_unidad',
    )
    list_filter = ('activo_unidad',)
    search_fields = ('codigo_unidad', 'nombre_unidad', 'simbolo_unidad', 'descripcion_unidad')
    readonly_fields = ('id_unidad_medida',)

@admin.register(MenuProductos)
class MenuProductos(admin.ModelAdmin):
    list_display = (
        'id_producto',
        'id_categoria',
        'id_unidad_medida',
        'nombre_producto',
        'sku_producto',
        'descripcion_producto',
        'stock_actual_producto',
        'stock_minimo_producto',
        'stock_maximo_producto',
        'ubicacion_producto',
        'imagen_url_producto',
        'activo_producto',
        'fecha_creacion_producto',
        'fecha_actualizacion_producto',
    )
    list_filter = ('activo_producto',)
    search_fields = ('nombre_producto','sku_producto','descripcion_producto')
    readonly_fields = ('id_producto',)


@admin.register(MenuLotes)
class MenuLotesAdmin(admin.ModelAdmin):
    list_display = (
        'id_lote',
        'id_producto',
        'numero_lote',
        'cantidad_recibida_lote',
        'cantidad_disponible_lote',
        'precio_compra_lote',
        'precio_venta_lote',
        'ganancia_formateada',  # Mostrar ganancia formateada en la lista
        'fecha_vencimiento_lote',
        'fecha_ingreso_lote',
        'id_proveedor',
        'activo_lote',
        'observaciones_lote',
    )
    list_filter = ('activo_lote', 'fecha_vencimiento_lote')
    search_fields = ('numero_lote', 'id_producto__nombre_producto', 'id_producto__sku_producto')
    
    # Hacer readonly TODOS los campos calculados
    readonly_fields = ('id_lote', 'porcentaje_ganancia_lote', 'ganancia_formateada')
    
    # Personalizar el formulario para mostrar los campos calculados como solo lectura
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'id_producto',
                'numero_lote',
                'cantidad_recibida_lote',
                'cantidad_disponible_lote',
                'precio_compra_lote',
                'precio_venta_lote',
                'id_proveedor',
            )
        }),
        ('Ganancias (Calculadas automáticamente)', {
            'fields': ('porcentaje_ganancia_lote', 'ganancia_formateada'),
            'classes': ('collapse',),  # Sección colapsable
        }),
        ('Información Adicional', {
            'fields': (
                'fecha_vencimiento_lote',
                'fecha_ingreso_lote',
                'activo_lote',
                'observaciones_lote',
            )
        }),
    )




@admin.register(CatTiposMovimiento)
class CatTiposMovimientoAdmin(admin.ModelAdmin):
    list_display = (
        'id_tipo_movimiento',
        'codigo_tipo',
        'nombre_tipo',
        'signo',
        'requiere_precio',
        'activo',
        'orden',
    )
    list_filter = ('activo', 'requiere_precio')
    search_fields = ('codigo_tipo', 'nombre_tipo', 'descripcion')
    readonly_fields = ('id_tipo_movimiento',)


@admin.register(MenuHistorialPrecios)
class MenuHistorialPreciosAdmin(admin.ModelAdmin):
    list_display = (
        'id_historial_precio',
        'id_producto',
        'id_lote',
        'precio_compra_anterior',
        'precio_compra_nuevo',
        'precio_venta_anterior',
        'precio_venta_nuevo',
        'fecha_cambio_precio',
        'usuario_cambio',
    )
    list_filter = ('fecha_cambio_precio',)
    search_fields = ('id_producto__nombre_producto', 'id_producto__sku_producto', 'usuario_cambio', 'motivo_cambio')
    readonly_fields = ('id_historial_precio',)


@admin.register(MenuMovimientos)
class MenuMovimientosAdmin(admin.ModelAdmin):
    list_display = (
        'id_movimiento',
        'id_producto',
        'id_lote',
        'tipo_movimiento',
        'cantidad_movimiento',
        'precio_unitario_movimiento',
        'fecha_movimiento',
        'id_tipo_movimiento',
        'usuario_id',
    )
    list_filter = ('tipo_movimiento', 'fecha_movimiento', 'id_tipo_movimiento')
    search_fields = (
        'id_producto__nombre_producto',
        'id_producto__sku_producto',
        'motivo_movimiento',
        'documento_referencia_movimiento',
        'usuario_id__nombreusuario',
    )
    readonly_fields = ('id_movimiento',)
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': (
                'id_producto',
                'id_lote',
                'id_tipo_movimiento',
                'tipo_movimiento',
                'cantidad_movimiento',
                'precio_unitario_movimiento',
            )
        }),
        ('Detalles Adicionales', {
            'fields': (
                'fecha_movimiento',
                'motivo_movimiento',
                'documento_referencia_movimiento',
                'observaciones_movimiento',
            )
        }),
        ('Auditoría', {
            'fields': ('usuario_id', 'id_movimiento'),
            'classes': ('collapse',)
        }),
    )
